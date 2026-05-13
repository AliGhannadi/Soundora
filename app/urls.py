from django.urls import path, include

app_name = "app"


urlpatterns = [
    path("api/v1/", include("app.api.v1.urls")),
]
