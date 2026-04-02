from django.urls import path
from . import views

# from rest_framework.authtoken.views import obtain_auth_token
app_name = "api-v1"

urlpatterns = [
    path(
        "test/",
        views.Test.as_view(),
        name="test",
    )
]