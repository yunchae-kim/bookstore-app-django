from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Book, CustomUser


# Custom UserAdmin class for the CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    # Additional fieldsets for the CustomUser model including 'author_pseudonym'
    fieldsets = list(BaseUserAdmin.fieldsets) + [
        (_("Additional Info"), {"fields": ("author_pseudonym",)}),
    ]
    # Fields to display in the list view for CustomUser objects
    list_display = ("username", "email", "first_name", "last_name", "author_pseudonym")
    # Fields that can be searched in the admin list view for CustomUser objects
    search_fields = ("username", "email", "first_name", "last_name", "author_pseudonym")


# Custom Admin class for the Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view for Book objects
    list_display = (
        "title",
        "author",
        "price",
    )
    # Fields that can be searched in the admin list view for Book objects
    search_fields = (
        "title",
        "author__username",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "author",
                    "cover_image",
                    "price",
                ),
                "description": "These fields are related to the book details.",
            },
        ),
    )
