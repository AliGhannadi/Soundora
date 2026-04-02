from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import MusicSerializer
from app.models import Music

class MusicListView(ListAPIView):
    queryset = Music.objects.filter(is_published=True)
    serializer_class = MusicSerializer

class MusicRetreiveView(RetrieveAPIView):
    queryset = Music.objects.filter(is_published=True)
    serializer_class = MusicSerializer    