from django.contrib import admin
from .models import Music , Category

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "producer", "cover_image", "created_date"]
    list_filter = ["name", "category", "producer"]
    ordeirng = ("pk")
    



admin.site.register(Category)