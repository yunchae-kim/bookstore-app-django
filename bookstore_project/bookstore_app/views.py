from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, viewsets

from .models import Book
from .permissions import IsAdmin, IsAuthor, IsNotBanned
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
        # Allow only authenticated users and authors to perform POST operations
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated, IsNotBanned, IsAuthor]
        # Allow only admins to perform PUT operations
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsNotBanned, IsAdmin]
        # Allow only admins and authors of own book to perform DELETE operations
        elif self.action == "destroy":
            permission_classes = [IsNotBanned, IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    # Set the author to the current user during book creation
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
