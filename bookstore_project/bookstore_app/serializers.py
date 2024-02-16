from django.contrib.auth import get_user_model
from rest_framework import serializers

from .mixins import DisplayNameMixin
from .models import Book

User = get_user_model()


class UserSerializer(DisplayNameMixin, serializers.ModelSerializer):
    displayed_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "displayed_name"]


class BookSerializer(DisplayNameMixin, serializers.ModelSerializer):
    displayed_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "displayed_name",
            "cover_image",
            "price",
        ]
