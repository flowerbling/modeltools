import os


def get_env_setting(key: str) -> str:
    value = os.environ.get(key, "")
    return value
