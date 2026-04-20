import django_filters
from app.models import Music

class MusicFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains"
    )
    artist_name = django_filters.CharFilter(
        field_name="artist__user__username",
        lookup_expr="icontains"
    )
    lyrics = django_filters.CharFilter(
        field_name="lyrics",
        lookup_expr="icontains"
    )
    created_after = django_filters.DateFilter(
        field_name="uploaded_at",
        lookup_expr="gte"
    )
    created_before = django_filters.DateFilter(
        field_name="uploaded_at",
        lookup_expr="lte"
        
    )
    class Meta:
        model = Music
        fields = ["title", "artist_name"]
        fields = {
            "category": ["exact"],
            "artist": ["in", "exact"],
            "uploaded_at": ["exact"],
            
        }