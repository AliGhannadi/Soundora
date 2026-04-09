import django_filters
from app.models import Music

class MusicFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )
    producer_name = django_filters.CharFilter(
        field_name="producer__user__username",
        lookup_expr="icontains"
    )
    lyrics = django_filters.CharFilter(
        field_name="lyrics",
        lookup_expr="icontains"
    )
    created_after = django_filters.DateFilter(
        field_name="created_date",
        lookup_expr="gte"
    )
    created_before = django_filters.DateFilter(
        field_name="created_date",
        lookup_expr="lte"
        
    )
    class Meta:
        model = Music
        fields = ["name", "producer_name"]
        fields = {
            "is_published": ["exact"],
            "category": ["exact"],
            "producer": ["in", "exact"],
            
        }