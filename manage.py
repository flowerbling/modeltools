#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import find_dotenv, load_dotenv


def init():
    """
        Init the environ from env file
    """
    env_path = find_dotenv()
    env = os.environ.get("ENV")
    if env:
        p = f'{env_path}.{env}'
        if os.path.exists(p):
            env_path = p

    load_dotenv(env_path)


def main():
    """Run administrative tasks."""
    init()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modeltools.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()