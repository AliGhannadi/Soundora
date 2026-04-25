import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def valid_user_data():
    return {
        "first_name": "Ali",
        "last_name": "Alavi",
        "username": "alialavi",
        "email": "ali@example.com",
        "phone_number": "09123456789",
        "password": "StrongPassword123!",
        "password1": "StrongPassword123!"
    }

@pytest.fixture
def create_verified_user(db):
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!"
    )
    user.is_active = True
    user.is_verified = True 
    user.save()
    return user


@pytest.mark.django_db
class TestRegistrationAPI:

    def test_register_success(self, api_client, valid_user_data):
        url = reverse("users:api-v1:register")
        response = api_client.post(url, valid_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="alialavi").exists()
        
    def test_register_password_mismatch(self, api_client, valid_user_data):
        valid_user_data["password1"] = "DifferentPassword123!"
        url = reverse("users:api-v1:register")
        response = api_client.post(url, valid_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.data
        assert response.data["detail"] == "Passwords dont match."

    def test_register_weak_password(self, api_client, valid_user_data):
        valid_user_data["password"] = "123"
        valid_user_data["password1"] = "123"
        url = reverse("users:api-v1:register")
        response = api_client.post(url, valid_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data
        assert isinstance(response.data["password"], list)


@pytest.mark.django_db
class TestLoginAPI:

    def test_login_success(self, api_client, create_verified_user):
        url = reverse("users:api-v1:login")
        data = {
            "username": "testuser",
            "password": "TestPassword123!"
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["username"] == "testuser"
        assert response.data["message"] == "Welcome to soundora!"

    def test_login_wrong_credentials(self, api_client, create_verified_user):
        url = reverse("users:api-v1:login")
        data = {
            "username": "testuser",
            "password": "WrongPassword!"
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "username or password is incorrect."

    def test_login_inactive_user(self, api_client, create_verified_user):
        create_verified_user.is_active = False
        create_verified_user.save()
        
        url = reverse("users:api-v1:login")
        data = {
            "username": "testuser",
            "password": "TestPassword123!"
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Your account is not activated."

    def test_login_unverified_user(self, api_client, create_verified_user):
        create_verified_user.is_verified = False
        create_verified_user.save()
        
        url = reverse("users:api-v1:login")
        data = {
            "username": "testuser",
            "password": "TestPassword123!"
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Your account is not verified yet."

    def test_login_missing_fields(self, api_client):
        url = reverse("users:api-v1:login")
        response = api_client.post(url, {})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data
        assert "password" in response.data
