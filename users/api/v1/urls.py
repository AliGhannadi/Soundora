from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework.authtoken.views import obtain_auth_token
app_name = "api-v1"

urlpatterns = [
    path(
        "test/",
        views.Test.as_view(),
        name="test",
    ),
    path("register/", views.RegistratrionAPIView.as_view(), name="register"),
    path("token/login/", views.LoginAPIView.as_view(), name="login"),
    path("token/refresh-v1", TokenRefreshView.as_view(), name="refresh-v1"),
    path("token/refresh-v2", views.CustomRefreshTokenAPIView.as_view(), name="refresh-v2"),
    path("me/<int:pk>", views.UserAPIView.as_view(), name="profile"),

]