from os import getenv


def get_env(key: str):
    e = getenv(key)
    if not e:
        return ""
    return e
