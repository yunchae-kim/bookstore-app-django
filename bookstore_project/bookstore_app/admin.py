from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .forms import BookForm
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
    form = BookForm
    # Fields to display in the list view for Book objects
    list_display = (
        "title",
        "author",
        "price",
        "displayed_name",
    )
    # Fields that can be searched in the admin list view for Book objects
    search_fields = (
        "title",
        "author__username",
        "displayed_name",
    )

    # Define custom fieldsets
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
                    "displayed_name",
                ),
                "description": "These fields are related to the book details.",
            },
        ),
        (
            "Author Identity",
            {
                "fields": ("use_pseudonym",),
                "description": "Control how the author's identity is displayed. This choice will not be saved with the book record.",
            },
        ),
    )

    # Retrieve the author's preference for using a pseudonym from the form
    def save_model(self, request, obj, form, change):
        author = obj.author

        # Ensure 'author' is not None before attempting to set 'displayed_name'
        if author is not None:
            use_pseudonym = form.cleaned_data.get("use_pseudonym", False)

            if use_pseudonym and author.author_pseudonym:
                # Set displayed_name to the author's pseudonym if selected
                obj.displayed_name = author.author_pseudonym
            elif author.first_name and author.last_name:
                # Otherwise, use the author's real name
                obj.displayed_name = f"{author.first_name} {author.last_name}".strip()
            else:
                # If no valid name or pseudonym is available, set as "Unknown Author"
                obj.displayed_name = _("Unknown Author")

        super().save_model(request, obj, form, change)
