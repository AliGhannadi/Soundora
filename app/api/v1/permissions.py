
from rest_framework import permissions

class IsArtistOfSong(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        # View-level check: Anyone can access the list/view itself
        # You could restrict this further if needed.
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_verified)

        # Write permissions are only allowed to the owner of the snippet.
        # This checks if the user making the request is the same as the object's owner.
        return bool(obj.is_artist and request.user and request.user.is_verified)
    
class IsArtist(permissions.BasePermission):
    def has_permission(self, request, view):
           if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_verified)
           return bool(request.user and request.user.is_verified and request.user.is_artist)


