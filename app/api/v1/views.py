from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import MusicListSerializer, MusicDetailSerializer, PlayListSerializer
from app.models import Music, PlayList, Like
from .pagination import Pagination
from .filters import MusicFilter
from .permissions import IsArtist, IsOwnerOrReadOnly
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.db import transaction

@method_decorator(cache_page(60 * 5, cache="page_cache", key_prefix="music_list"), name="list")
@method_decorator(vary_on_headers("Authorization"), name="list")
class MusicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Music.objects.filter(is_published=True)
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MusicFilter
    def get_serializer_class(self):
        if self.action == "list":
            return MusicListSerializer
        if self.action == "retrieve":
            return MusicDetailSerializer

    # @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    # def like(self, request, pk=None):
    #     music = self.get_object()
    #     user = request.user

    #     if user in music.likes.all():
    #         music.likes.remove()
    #         message = 'Music unliked.'
    #         is_liked = False
    #     else:
    #         music.likes.add(user)
    #         message = "Music liked."
    #         is_liked = True
    #     return Response({
    #         "message": message,
    #         "likes_count": music.likes.count(),
    #         "is_liked": is_liked
    #     }, status=status.HTTP_200_OK)
    # Optional action instead of using seperate model and view for like


class ArtistPanelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsArtist, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "artist"):
            return Music.objects.filter(artist=user.artist)
        return Music.objects.none()

    def get_serializer_class(self):
        if self.action == "list":
            return MusicListSerializer
        if self.action == "retrieve":
            return MusicDetailSerializer
        return MusicDetailSerializer

    def perform_create(self, serializer):
        user = self.request.user
        artist = user.artist
        serializer.save()
        serializer.instance.artist.add(artist)


class PlayListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    serializer_class = PlayListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return PlayList.objects.filter(Q(is_public=True) | Q(owner=user))
        return PlayList.objects.filter(is_public=True)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)


class ToggleLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, music_id):
        try:
            music = Music.objects.get(pk=music_id)
        except Music.DoesNotExist:
            return Response(
                {"detail": "Music not found"}, status=status.HTTP_404_NOT_FOUND
            )
        like, is_created = Like.objects.get_or_create(user=request.user, music=music)
        if is_created:
            like.delete()
            message = "Like has been deleted."
            is_liked = False
        else: 
            Like.objects.create(user=request.user, music=music)
            message = "Music has been liked."
            is_liked = True
            

        return Response(
            {
                "message": message,
                "is_liked": is_liked,
            }
        )
