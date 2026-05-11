from rest_framework import viewsets, generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import MusicListSerializer, MusicDetailSerializer, PlayListSerializer
from app.models import Music, PlayList
from users.models import Artist
from .pagination import Pagination
from .filters import MusicFilter
from .permissions import IsArtist, IsOwnerOrReadOnly
from rest_framework import serializers
from django.db.models import Q

class MusicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Music.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MusicFilter
    def get_serializer_class(self):
        if self.action == 'list':
            return MusicListSerializer
        if self.action == 'retrieve':
            return MusicDetailSerializer
        
        
class ArtistPanelViewSet(viewsets.ModelViewSet):
     permission_classes = [IsArtist, IsAuthenticated]
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
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    serializer_class = PlayListSerializer
    pagination_class = Pagination
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
           return PlayList.objects.filter(
               Q(is_public=True) | Q(owner=user)
           )
        return PlayList.objects.filter(is_public=True)
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)
    
     
    