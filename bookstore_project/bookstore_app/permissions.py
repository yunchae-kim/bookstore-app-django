from rest_framework import permissions

from .banned_users_cache import get_banned_users


# Custom permission to check if the user is banned
class IsNotBanned(permissions.BasePermission):
    def has_permission(self, request, view):

        # Skip permission check for non-authenticated users
        if not request.user or not request.user.is_authenticated:
            return True

        banned_users = get_banned_users()

        # User is not allowed if they are in the banned users list
        return request.user.username not in banned_users


# Custom permission to check if the user is the author of a book
class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
