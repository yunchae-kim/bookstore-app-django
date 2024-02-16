from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Book, CustomUser


# Custom form for changing existing user details in the admin
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"  # Include all fields from the CustomUser model


# Custom form for creating a new user in the admin
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # Fields to be included in the user creation form
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "author_pseudonym",
        )


# Custom UserAdmin class for the CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm  # Use the custom user change form
    add_form = CustomUserCreationForm  # Use the custom user creation form

    # Additional fieldsets for the CustomUser model including 'author_pseudonym'
    fieldsets = list(BaseUserAdmin.fieldsets) + [
        (_("Publication Information"), {"fields": ("author_pseudonym",)}),
    ]

    # Fields to display in the list view for CustomUser objects
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "author_pseudonym",
    )

    # Fields that can be searched in the admin list view for CustomUser objects
    search_fields = ("username", "email", "first_name", "last_name", "author_pseudonym")


# Custom Admin class for the Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view for Book objects
    list_display = ("title", "author", "price")

    # Fields that can be searched in the admin list view for Book objects
    search_fields = (
        "title",
        "author__username",
        "author__email",
        "author__first_name",
        "author__last_name",
        "author__author_pseudonym",
    )
