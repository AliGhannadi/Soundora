from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from users.models import User
from .serializers import RegistrationSerializer, LoginSerializer, RefreshTokenSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import status
from django.shortcuts import get_object_or_404
class Test(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"detail": "ok"})
    
    
class RegistratrionAPIView(CreateAPIView):
    serializer_class = RegistrationSerializer
    
    
class LoginAPIView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        data = {
        "email": user.email, 
        "refresh": str(refresh),
        "access": access,
                }
        return Response(data)
    
class CustomRefreshTokenAPIView(generics.GenericAPIView):
    serializer_class = RefreshTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            user_id = refresh["user_id"]
            user = User.objects.get(pk=user_id)
            new_access = str(refresh.access_token)
            refresh.blacklist()
            new_refresh = str(RefreshToken.for_user(user))
            data = {
                "access: ": new_access,
                "refresh: ": new_refresh
            }
            return Response(data)
        except User.DoesNotExist:
            return Response({"detail": "No user found."})      
        except (InvalidToken, TokenError):
            return Response(
                {"detail": "Refresh token is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    # def get_queryset(self):
    #     return User.objects.all()
    
    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(queryset, pk=self.request.user.pk)
    #     return obj
    def get_object(self):
        return self.request.user
        
        
        