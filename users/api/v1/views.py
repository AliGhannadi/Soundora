from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from users.models import User
from .serializers import RegistrationSerializer, LoginSerializer, RefreshTokenSerializer, UserSerializer, SMSVerificationSerializer, SMSVerificationResendSerializer
from users.api.sms import sms_message
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import status
from djoser.views import UserViewSet
from rest_framework.decorators import action
from django.utils.http import urlsafe_base64_decode
from djoser import email
from django.contrib.auth.tokens import default_token_generator

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
    
class SMSVerificationAPIView(generics.GenericAPIView):
    serializer_class = SMSVerificationSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "User has been verified."}, status=status.HTTP_200_OK)
    
class SMSVerificationResendAPIView(generics.GenericAPIView):
    serializer_class = SMSVerificationResendSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "Code has been sent."})
    

class CustomUserViewSet(UserViewSet):
    def perform_activation(self, user):
        user.is_verified = True
        user.save()
    def activation(self, request, *args, **kwargs):
            uid = request.data.get("uid")
            token = request.data.get("token")
            try:
             decoded_uid = urlsafe_base64_decode(uid).decode()
             user = User.objects.get(pk=decoded_uid)
            except (User.DoesNotExist, TypeError, ValueError, OverflowError):
               return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
           
            if user.is_verified: # Checks if user verified or not
                return Response({"detail": "User is already verified."}, status=status.HTTP_400_BAD_REQUEST)
            
            is_token_valid = default_token_generator.check_token(user, token) # Custom verification for token, because we use is_verified instead of is_active
            if not is_token_valid:
                return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
            
            self.perform_activation(user) # sets is_verified true
            return Response({"detail": "User verified."}, status=status.HTTP_200_OK)
    @action(["post"], detail=False)
    def resend_activation(self, request):
        email_value = request.data.get("email")
        try: 
            user = User.objects.get(email=email_value)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if user.is_verified:
            return Response({"detail": "User is already verified."}, status=status.HTTP_400_BAD_REQUEST)
        context = {"user": user}
        to_email = [user.email]
        email.ActivationEmail(request, context).send(to_email)
        return Response({"detail": "Activation email sent"}, status=status.HTTP_200_OK)
         
        
        
        