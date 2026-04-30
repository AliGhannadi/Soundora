from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Artist
from app.models import Music
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "first_name", "last_name", "username", "phone_number", "is_superuser", "is_active", "is_verified")
    list_filter = ("email", "username", "phone_number", "is_superuser", "is_active")
    search_fields = ("email", "username",  "phone_number", "is_superuser", "is_active")
    ordering = ("pk",)
    actions = ["deactivate_user"]
    def deactivate_user(self, request, queryset):
        queryset.update(is_active=False)
    fieldsets = (
        (None, {"fields": ("email", "phone_number", "password", "username")}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "is_artist",
                )
            },
        ),
        ("Group Permissions", {"fields": ("groups", "user_permissions")}),
        ("Last Login", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "username",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ],
            },
        ),
    )

class MusicInline(admin.TabularInline):
    model = Music.artist.through
    extra = 1
    
class ProducerAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "played_time", "website", "location", "is_suspended", "rating"]
    list_filter = ["user", "category", "is_suspended", "location"]
    search_fields = ["user__username", "category", "pk"]
    ordering = ("pk",)
    inlines = [MusicInline]
    actions = ["suspend_producer"]
    def suspend_producer(self, request, queryset):
        queryset.update(is_suspended=True)

admin.site.register(Artist, ProducerAdmin)
admin.site.register(User, CustomUserAdmin)