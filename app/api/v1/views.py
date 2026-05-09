from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import MusicListSerializer, MusicDetailSerializer, PlayListSerializer
from app.models import Music, PlayList
from users.models import Artist
from .pagination import MusicPagination
from .filters import MusicFilter
from .permissions import IsArtist
from rest_framework import serializers
class MusicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Music.objects.all()
    permission_classes = []
    pagination_class = MusicPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MusicFilter
    def get_serializer_class(self):
        if self.action == 'list':
            return MusicListSerializer
        if self.action == 'retrieve':
            return MusicDetailSerializer
        
        
class ArtistPanelViewSet(viewsets.ModelViewSet):
     permission_classes = [IsArtist]
     def get_queryset(self):
         user = self.request.user
         if hasattr(user, 'artist'):
             return Music.objects.filter(artist=user.artist)
         return Music.objects.none()
     def get_serializer_class(self):
        if self.action == 'list':
            return MusicListSerializer
        if self.action == 'retrieve':
            return MusicDetailSerializer
        return MusicDetailSerializer
     def perform_create(self, serializer):
        user = self.request.user
        artist = user.artist
        serializer.save(artist=[artist])
        
class PlayListViewSet(viewsets.ModelViewSet):
    serializer_class = [PlayListSerializer]
    def get_queryset(self):
        return PlayList.objects.all()
    
     
    