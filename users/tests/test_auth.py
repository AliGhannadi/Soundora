import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_credentials():
    return {"email": "newww1234user@example.com", "password": "ali1234567pytest"}


@pytest.fixture
def create_user(db, user_credentials):
    user = User.objects.create_user(
        email=user_credentials["email"], password=user_credentials["password"]
    )
    return user


@pytest.mark.django_db
class TestAPIEndpoints:

    def test_test_endpoint(self, api_client):
        url = reverse("users:api-v1:test")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"detail": "ok"}

    def test_registration_endpoint(self, api_client):
        url = reverse("users:api-v1:register")
        payload = {
            "first_name": "Pytest",
            "last_name": "Lovewr",
            "username": "pytesttest",
            "email": "newwwuser@example.com",
            "phone_number": "09999998",
            "password": "ali1234567pytest",
            "password1": "ali1234567pytest",
        }

        response = api_client.post(url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="newwwuser@example.com").exists()

    def test_login_endpoint_success(self, api_client, create_user, user_credentials):
        url = reverse("users:api-v1:login")

        response = api_client.post(url, user_credentials)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_endpoint_invalid_credentials(self, api_client, create_user):
        url = reverse("users:api-v1:login")
        payload = {"email": "testuser@example.com", "password": "wrong_password"}

        response = api_client.post(url, payload)

        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
        ]

    def test_custom_refresh_token_endpoint_success(self, api_client, create_user):
        url = reverse("users:api-v1:refresh-v2")
        refresh = RefreshToken.for_user(create_user)

        payload = {"refresh": str(refresh)}

        response = api_client.post(url, payload)

        assert response.status_code == status.HTTP_200_OK
        # در کد اصلی ویو شما، کلیدها دارای فاصله هستند ("access: ")
        assert "access: " in response.data
        assert "refresh: " in response.data

    def test_custom_refresh_token_endpoint_invalid_token(self, api_client):
        url = reverse("users:api-v1:refresh-v2")
        payload = {
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid_token_payload.signature"
        }

        response = api_client.post(url, payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "Refresh token is invalid or expired"
