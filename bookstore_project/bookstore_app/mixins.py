class DisplayNameMixin:
    # Method to determine the user's displayed name
    def get_displayed_name(self, user):
        # Check if the user prefers to use a pseudonym
        if user.author_pseudonym:
            return user.author_pseudonym
        else:
            return (
                # If the user does not have a pseudonym, use the user's real name if available
                f"{user.first_name} {user.last_name}".strip()
                if user.first_name and user.last_name
                # Otherwise, use the username
                else user.username
            )
