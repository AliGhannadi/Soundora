from django.db import models
from users.models import Artist, User
from django.urls import reverse
import uuid
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.urls import reverse
from .utils import extract_music_metadata
from django.core.exceptions import ValidationError
from django.http import HttpResponse

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Album(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Music(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="musics",
        blank=True, null=True
        
    )
    artist = models.ManyToManyField(
        Artist,
        related_name="artist",
        blank=True
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="musics",
        blank=True, null=True
    )
    cover_image = models.ImageField(upload_to="cover-images/", blank=True, null=True)
    lyrics = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    file = models.FileField(upload_to="musics/")
    auto_fill_title = models.BooleanField(default=True, verbose_name="Title Auto-Fill")
    auto_fill_album = models.BooleanField(default=True, verbose_name="Album Auto-Fill")
    auto_fill_coverimage = models.BooleanField(default=True, verbose_name="CoverImage Auto-Fill")
    auto_fill_artist = models.BooleanField(default=True, verbose_name="Producer Auto-Fill")
    auto_fill_artist = models.BooleanField(default=True, verbose_name="Artist Auto-Fill")
    
    def get_absolute_api_url(self):
        return reverse("app:api-v1:music-detail", kwargs={"pk": self.id})
    def __str__(self):
        return self.title or "Unknown Track"
    
    # Overriding save method for saving the musics
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            super().save(*args, **kwargs)
        if self.file:
          file_path = self.file.path
          metadata = extract_music_metadata(file_path)
          if metadata:
                need_update=False
                if not self.title and metadata.get("title") and self.auto_fill_title:
                        self.title = metadata.get('title')
                        need_update=True
                if not self.album and metadata.get("album") and self.auto_fill_album:
                        album, _ = Album.objects.get_or_create(name=metadata.get('album'))
                        self.album = album
                        need_update=True
                if not self.cover_image and self.auto_fill_coverimage:
                        # handles the cover image conversion
                        image_data = metadata.get('cover_image_data')
                        mime_type = metadata.get('cover_mime_type')
                        if image_data:
                            ext = 'jpg'
                            if mime_type == 'image/png':
                                ext = 'png'
                            filename = f"cover_{uuid.uuid4().hex[:8]}.{ext}"
                            django_file = ContentFile(image_data, name=filename)
                            self.cover_image.save(filename, django_file, save=False)
                        need_update=True
                        
                # Updating regular fields
                if need_update:
                    super().save(update_fields=['title', 'album', 'cover_image'])
                    
