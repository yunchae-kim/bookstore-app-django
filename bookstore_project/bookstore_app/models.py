from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    author_pseudonym = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Author Pseudonym",
        help_text="Enter author pseudonym (max 30 characters).",
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

    def __str__(self):
        return self.title
