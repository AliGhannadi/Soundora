from django.contrib import admin
from .models import Music , Category

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "producer", "cover_image", "uploaded_at"]
    list_filter = ["title", "category", "producer"]
    ordeirng = ("pk")
    



admin.site.register(Category)