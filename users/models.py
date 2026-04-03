from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email Required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
          raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
          raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email=email, password=password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    avatar = models.ImageField(upload_to="avatars/")
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_producer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    notifications = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=11)
    
    objects = UserManager()
    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"
    
class Producer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="producer"
    )
    category = models.ForeignKey(
        "app.Category",
        on_delete=models.CASCADE,
        related_name="producer"
    )
    played_time = models.PositiveIntegerField(default=0)
    website = models.URLField(blank=True, null=True)
    location = CountryField()
    is_suspended = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} {self.user.last_name}"