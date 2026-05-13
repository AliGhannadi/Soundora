from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

# from rest_framework.authtoken.views import obtain_auth_token
app_name = "api-v1"

router = DefaultRouter()
router.register(r"music", views.MusicViewSet, basename="music")
router.register(r"artist", views.ArtistPanelViewSet, basename="artist-panel")
router.register(r"playlists", views.PlayListViewSet, basename="playlist")
urlpatterns = router.urls
urlpatterns += [
    path("toggle-like/<int:music_id>", views.ToggleLikeView.as_view(), name="like"),
]
