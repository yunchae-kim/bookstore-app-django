from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, viewsets

from .models import Book
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
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
