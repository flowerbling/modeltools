import os

import django


def main() -> None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modeltools.settings')
    django.setup()


if __name__ == "__main__":
    main()
