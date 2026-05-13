from rest_framework import permissions


class IsArtist(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_artist
            and getattr(request.user, "is_verified", False)
            and getattr(request.user, "is_artist", False)
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
        ):  # SAFE_METHOD is a tuple of read-only methods
            return True

        return obj.owner == request.user
