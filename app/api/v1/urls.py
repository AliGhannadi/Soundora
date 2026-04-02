from django.urls import path
from . import views

# from rest_framework.authtoken.views import obtain_auth_token
app_name = "api-v1"

urlpatterns = [
    path(
        "music/",
        views.MusicListView.as_view(),
        name="music-list"),
    path("music/<int:pk>/", views.MusicRetreiveView.as_view(), name="music-get")
]