from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email Required")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save()
        
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    avatar = models.ImageField(upload_to="avatars/")
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_producer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    notifications = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=11)
    
    objects = UserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    
class Producer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="producer"
    )
    category = models.CharField(max_length=60)
    played_time = models.IntegerField(default=0)
    website = models.URLField()
    location = models.CharField(max_length=20)
    is_suspended = models.BooleanField(default=0)
    rating = models.FloatField()