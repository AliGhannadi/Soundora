from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import MusicListSerializer, MusicDetailSerializer
from app.models import Music
from .pagination import MusicPagination
class MusicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Music.objects.all()
    permission_classes = []
    pagination_class = MusicPagination
    def get_serializer_class(self):
        if self.action == 'list':
            return MusicListSerializer
        if self.action == 'retrieve':
            return MusicDetailSerializer