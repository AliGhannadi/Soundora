from django.contrib import admin
from .models import Music , Category, Album
from django.contrib import messages
from .utils import extract_music_metadata
from django.contrib.auth.hashers import make_password
from .models import User, Artist
@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "get_artists", "cover_image", "uploaded_at", "file"]
    list_filter = ["title", "category"]
    ordering = ("pk",)
    readonly_fields = ["get_artists"]
    filter_horizontal = ["artist"] 
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
                                                                     defaults={
                                                                         'username': artist_username,
                                                                         'password': make_password("123456")
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



admin.site.register(Category)
admin.site.register(Album)