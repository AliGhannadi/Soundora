from django.contrib import admin
from .models import Music , Category, Album, Stats, Like
from django.contrib import messages
from django.urls import path
from django.shortcuts import render
from .utils import extract_music_metadata
from django.contrib.auth.hashers import make_password
from .models import User, Artist
import random

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    def fake_iran_phone(self):
      return "09" + "".join(str(random.randint(0, 9)) for _ in range(9))

    list_display = ["title", "get_categories", "get_artists", "cover_image", "uploaded_at", "file"]
    list_filter = ["title", "category"]
    ordering = ("pk",)
    readonly_fields = ["get_artists"]
    filter_horizontal = ["artist"]
    def get_categories(self, obj):
        return ", ".join([p.category for p in obj.category.all()])
    def get_artists(self, obj):
        return ", ".join([p.user.username for p in obj.artist.all()])
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if not change and form.instance.file:
          obj = form.instance
          metadata = extract_music_metadata(obj.file.path)
          if not obj.artist.exists() and obj.auto_fill_artist:
                        artist_obj = metadata.get("artist")
                        if artist_obj and artist_obj.strip():
                                artist_username = artist_obj.replace(" ", "")
                                email = f"{artist_username}@admin.com"
                                user, _ = User.objects.get_or_create(email=email,
                                                                     defaults={ # If the user doesnt exist, it will be created with default username and password
                                                                         'username': artist_username,
                                                                         'password': make_password("123456"),
                                                                         'phone_number': self.fake_iran_phone(),
                                                                     })
                                artist, _ = Artist.objects.get_or_create(user=user)
                                obj.artist.add(artist) # because it is a m2m field
                            
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            self.message_user(
                request,
                f'🎵 "{obj.title}" - Make sure to manually change the password of the artist/producer if you enabled auto-filling and if the artist/producer user doesnt exist before.',
                messages.WARNING
            )
        else:
            self.message_user(
                request,
                f'🎵 "{obj.title}" Make sure to manually change the password of the artist/producer if you enabled auto-filling and if the artist/producer user doesnt exist before.',
                messages.WARNING
            )
    get_artists.short_description = "Artists"

@admin.register(Stats)
class StatsAdmin(admin.ModelAdmin):
    change_list_template = "admin/stats_change_list.html"  # custom template for page button

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("report/", self.admin_site.admin_view(self.stats_report), name="stats-report"),
        ]
        return custom_urls + urls

    def stats_report(self, request):
        stats = Stats.objects.first()  # Only one row expected
        total = (
            stats.win
            + stats.mac
            + stats.iphone
            + stats.android
            + stats.other
        ) or 1
        data = [
            {
                "name": "Windows",
                "value": stats.win,
                "percent": (stats.win / total) * 100,
                "color": "#4F46E5",
            },
            {
                "name": "Mac",
                "value": stats.mac,
                "percent": (stats.mac / total) * 100,
                "color": "#06B6D4",
            },
            {
                "name": "iPhone",
                "value": stats.iphone,
                "percent": (stats.iphone / total) * 100,
                "color": "#10B981",
            },
            {
                "name": "Android",
                "value": stats.android,
                "percent": (stats.android / total) * 100,
                "color": "#F59E0B",
            },
            {
                "name": "Other",
                "value": stats.other,
                "percent": (stats.other / total) * 100,
                "color": "#EF4444",
            },
        ]
        context = {
            "stats_data": data,
            "total": total,
            "title": "OS Statistics Report",
        }
        return render(request, "admin/stats_report.html", context)



admin.site.register(Category)
admin.site.register(Album)
admin.site.register(Like)