from os import getenv


def get_env(key: str, default: str = ""):
    e = getenv(key)
    if not e:
        return default
    return e
