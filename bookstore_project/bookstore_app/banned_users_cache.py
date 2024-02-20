banned_users_cache = {}


def set_banned_users(usernames):
    global banned_users_cache
    banned_users_cache["banned_users"] = usernames


def get_banned_users():
    return banned_users_cache.get("banned_users", [])
