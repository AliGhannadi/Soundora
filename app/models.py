from django.db import models
from users.models import Producer
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Music(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
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
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    file = models.FileField(upload_to="musics/")
    def get_absolute_api_url(self):
        return reverse("app:api-v1:music-detail", kwargs={"pk": self.id})
    def __str__(self):
        return self.title or "Unknown Track"