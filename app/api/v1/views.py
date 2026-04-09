from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import MusicListSerializer, MusicDetailSerializer
from app.models import Music
from .pagination import MusicPagination
from .filters import MusicFilter

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