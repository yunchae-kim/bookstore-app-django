from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Book

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    displayed_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "displayed_name"]

    def get_displayed_name(self, obj):
        if obj.author_pseudonym:
            return obj.author_pseudonym
        else:
            return obj.get_full_name() or obj.username


class BookSerializer(serializers.ModelSerializer):
    author_displayed_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "author",
            "cover_image",
            "price",
            "author_displayed_name",
        ]

    def get_author_displayed_name(self, obj):
        author = obj.author
        if author.author_pseudonym:
            return author.author_pseudonym
        else:
            return author.get_full_name() or author.username
