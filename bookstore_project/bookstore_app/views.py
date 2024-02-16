from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, viewsets

from .models import Book
from .permissions import IsAuthorToDelete
from .serializers import BookSerializer, UserSerializer

User = get_user_model()


# A viewset for viewing and editing user instances.
# Restricted to authenticated users only.
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# A viewset for viewing books. Allows unrestricted GET operations.
# Restricts POST, PUT, DELETE to authenticated users.
class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Allows dynamic filtering based on query parameters
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description", "author__username", "price"]

    # Define custom permissions for the BookViewSet
    def get_permissions(self):
        # Allow unrestricted GET operations
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        # Allow authenticated users to perform POST operations
        elif self.action in ["create", "update", "partial_update"]:
            permission_classes = [permissions.IsAuthenticated]
        # Allow authors to perform DELETE operations
        elif self.action == "destroy":
            permission_classes = [IsAuthorToDelete]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
