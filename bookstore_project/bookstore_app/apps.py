from django.apps import AppConfig

from .banned_users_cache import set_banned_users


class BookstoreAppConfig(AppConfig):
    name = "bookstore_app"

    def ready(self):
        banned_usernames = [
            "Darth Vader",
        ]
        set_banned_users(banned_usernames)
