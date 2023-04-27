import os
import json

def get_env_setting(key: str) -> str:
    value = os.environ.get(key, "")
    return value.__str__()


