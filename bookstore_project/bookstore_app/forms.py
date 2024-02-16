from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Book


class BookForm(forms.ModelForm):
    use_pseudonym = forms.BooleanField(
        required=False,
        label=_("Use Pseudonym"),
        help_text=_(
            "Select to display the author's pseudonym instead of real name. This choice will not be saved with the book record."
        ),
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "description",
            "author",
            "cover_image",
            "price",
            "displayed_name",
        ]

    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data.get("author")

        # Check that 'author' is not None before accessing its attributes
        if author is not None:
            use_pseudonym = cleaned_data.get("use_pseudonym", False)
            if use_pseudonym and author.author_pseudonym:
                cleaned_data["displayed_name"] = author.author_pseudonym
            elif author.first_name and author.last_name:
                cleaned_data["displayed_name"] = (
                    f"{author.first_name} {author.last_name}"
                )
            else:
                raise ValidationError(
                    _(
                        "Displayed identity cannot be blank. Please provide a pseudonym or ensure the author has a name."
                    )
                )
        else:
            # Handle case where 'author' might be None
            raise ValidationError(_("Author must be selected."))

        return cleaned_data
