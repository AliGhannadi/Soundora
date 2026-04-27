from rest_framework import serializers
from users.models import User, Artist
from app.api.v1.serializers import CategorySerializer
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from rest_framework import status
class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=200, write_only=True)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "phone_number", "password", "password1"]
    def validate(self, attrs):
        if(attrs.get("password") != attrs.get("password1")):
            raise serializers.ValidationError({"detail": "Passwords dont match."})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=200)
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if email and password:
            user = authenticate(request=self.context.get("request"),
                                email=email,
                                password=password)
            if not user:
                raise serializers.ValidationError({"detail": "email or password is incorrect."})
            if not user.is_active:
                raise serializers.ValidationError({"detail": "Your account is not activated."})
            if not user.is_verified:
                raise serializers.ValidationError({"detail": "Your account is not verified yet."})
        else:
            raise serializers.ValidationError({"detail": "email and password cant be empty."})
        
        attrs["user"] = user
        return attrs
    
class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255)

class ArtistSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Artist
        fields = ["user", "category", "played_time", "website", "location", "rating"]    
       
class UserSerializer(serializers.ModelSerializer):
    is_artist = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["avatar", "first_name", "last_name", "username", "email", "is_artist", "is_staff", "notifications", "phone_number"]
    def get_is_artist(self, obj):
        return obj.is_artist
    def to_representation(self, instance):
        request = self.context.get("request")
        data = super().to_representation(instance)
        if instance.is_artist:
            if hasattr(instance, 'artist'):
                artist_instance = instance.artist
                data["artist"] = ArtistSerializer(artist_instance, context=self.context).data
        return data
    # if is_artist:
    #     artist = ArtistSerializer(read_only=True)
    #     fields = ["avatar", "first_name", "last_name", "username", "email", "is_artist", "is_staff", "notificiation", "phone_number", "artist"]
    
        

            

    