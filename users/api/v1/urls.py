from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from djoser.views import UserViewSet
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
    path("me/", views.ProfileAPIView.as_view(), name="profile"),
    path("sms-verification/", views.SMSVerificationAPIView.as_view(), name="sms"),
    path("resend-sms-verification/", views.SMSVerificationResendAPIView.as_view(), name="resend-sms"),
    path("reset_password/", UserViewSet.as_view({"post": "reset_password"}, name="reset-password")),
    path("reset_password_confirm/", UserViewSet.as_view({"post": "reset_password_confirm"}, name="reset-password-confirm"))
]