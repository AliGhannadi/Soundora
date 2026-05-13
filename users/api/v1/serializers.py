import random
from rest_framework import serializers
from users.models import User, Artist
from app.api.v1.serializers import CategorySerializer
from users.api.sms import sms_message
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.core.cache import cache
from django.contrib.auth import authenticate
from djoser import email


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=200, write_only=True)
    sms_verification = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password",
            "password1",
            "sms_verification",
        ]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "Passwords dont match."})
        try:
            validate_password(attrs.get("password"))

        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data.pop("password1", None)
        sms_verification = validated_data["sms_verification"]
        validated_data.pop("sms_verification", None)
        user = User.objects.create_user(**validated_data)

        if sms_verification:
            phone_number = user.phone_number
            code = random.randint(1000, 9999)
            cache.set(f"verification_{phone_number}", code, timeout=300)
            sms_message(phone_number, code)
        else:
            context = {"user": user}
            to_email = [user.email]
            email.ActivationEmail(request, context).send(to_email)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=200)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if not user:
                raise serializers.ValidationError(
                    {"detail": "email or password is incorrect."}
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    {"detail": "Your account is not activated."}
                )
            if not user.is_verified:
                raise serializers.ValidationError(
                    {"detail": "Your account is not verified yet."}
                )
        else:
            raise serializers.ValidationError(
                {"detail": "email and password cant be empty."}
            )

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
        fields = [
            "avatar",
            "first_name",
            "last_name",
            "username",
            "email",
            "is_artist",
            "is_staff",
            "notifications",
            "phone_number",
        ]

    def get_is_artist(self, obj):
        return obj.is_artist

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_artist:
            if hasattr(instance, "artist"):
                artist_instance = instance.artist
                data["artist"] = ArtistSerializer(
                    artist_instance, context=self.context
                ).data
        return data

    # if is_artist:
    #     artist = ArtistSerializer(read_only=True)
    #     fields = ["avatar", "first_name", "last_name", "username", "email", "is_artist", "is_staff", "notificiation", "phone_number", "artist"]


class SMSVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        code = attrs.get("code")
        cached_code = cache.get(f"verification_{phone_number}")
        cache_key = f"verification_{phone_number}"
        #  attempts = cache.get(cache_key, 0)
        #  if attempts >= 15:
        #      raise serializers.ValidationError({"detail": "Limitation reached. Plaese try again later."})
        if cached_code is None:
            raise serializers.ValidationError(
                {"detail": "code is expired or not found or user is already verified."}
            )
        if str(cached_code) != str(code):
            raise serializers.ValidationError(
                {"detail": "Invalid verification code. try again."}
            )
        try:
            user = User.objects.get(phone_number=phone_number)
            user.is_verified = True
            user.save(update_fields=["is_verified"])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "No user found with this phone number"}
            )
        cache.delete(cache_key)
        return attrs


class SMSVerificationResendSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.is_verified:
                raise serializers.ValidationError(
                    {"detail": "This user is already verified."}
                )
            code = random.randint(1000, 9999)
            cache.set(f"verification_{phone_number}", code, timeout=300)
            sms_message(phone_number, code)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "No user found with this phone number"}
            )
        return attrs
