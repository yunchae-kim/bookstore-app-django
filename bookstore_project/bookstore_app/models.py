from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    # Add a new field to the CustomUser model to store the author's pseudonym
    author_pseudonym = models.CharField(
        max_length=100,
        unique=False,
        null=True,
        blank=True,
        verbose_name=_("Author Pseudonym"),
        help_text=_("Enter author pseudonym (max 100 characters)."),
    )

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Author")
    )
    cover_image = models.ImageField(
        upload_to="book_covers/", blank=True, null=True, verbose_name=_("Cover Image")
    )
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Price"))
    # Add a new field to the Book model to store the displayed identity (real name or pseudonym)
    displayed_name = models.CharField(
        max_length=100, blank=True, verbose_name=_("Displayed Name")
    )

    def __str__(self):
        return self.title
