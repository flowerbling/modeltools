import os

import django

from manage import init


def main() -> None:
    init()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    django.setup()


if __name__ == "__main__":
    main()
