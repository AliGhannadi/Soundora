from django.urls import path, include

app_name = "users"


urlpatterns = [
    path("api/v1/", include("app.api.v1.urls")),

]