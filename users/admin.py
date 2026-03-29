from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "first_name", "last_name", "username", "is_superuser", "is_active", "is_verified")
    list_filter = ("email", "username", "is_superuser", "is_active")
    search_fields = ("email", "username", "is_superuser", "is_active")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        # ('Personal Info', {'fields': ('first_name', 'last_name')}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
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


admin.site.register(User, CustomUserAdmin)