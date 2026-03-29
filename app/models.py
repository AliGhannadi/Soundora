from django.db import models
from users.models import Producer
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    
class Music(models.Model):
    name = models.CharField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="musics"
        
    )
    producer = models.ForeignKey(
        Producer,
        on_delete=models.CASCADE,
        related_name="musics"
    )
    cover_image = models.ImageField(upload_to="cover-images/")
    lyrics = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="musics/")