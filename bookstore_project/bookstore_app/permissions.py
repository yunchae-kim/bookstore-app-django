from rest_framework import permissions


class IsAuthorToDelete(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Allow read access
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow the author to delete the object
        if request.method == "DELETE":
            return obj.author == request.user

        # Default deny if not covered by any of the above.
        return False
