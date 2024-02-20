import json

from django.conf import settings
from rest_framework import permissions


# Custom permission to check if the user is banned
class IsNotBanned(permissions.BasePermission):
    def has_permission(self, request, view):
        banned_users_path = settings.BANNED_USERS_JSON_PATH
        user = request.user

        # Skip permission check for non-authenticated users
        if not user or not user.is_authenticated:
            return True

        with open(banned_users_path, "r") as f:
            banned_users = json.load(f)

        # User is not allowed if they are in the banned users list
        return user.username not in banned_users


class IsAuthorToDelete(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Allow read access
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow the author to delete the object if the user is not banned
        if request.method == "DELETE":
            return obj.author == request.user and IsNotBanned().has_permission(
                request, view
            )

        # Default deny if not covered by any of the above.
        return False
