import json

from django.conf import settings
from rest_framework import permissions


# Custom permission to check if the user is banned
def is_not_banned(user):
    banned_users_path = settings.BANNED_USERS_JSON_PATH

    with open(banned_users_path, "r") as f:
        banned_users = json.load(f)

    return user.username not in banned_users


class IsAuthorToDelete(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Allow read access
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow the author to delete the object if the user is not banned
        if request.method == "DELETE":
            return obj.author == request.user and is_not_banned(request.user)

        # Default deny if not covered by any of the above.
        return False
