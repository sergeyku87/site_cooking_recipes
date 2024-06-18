#!/usr/bin/env python
import os
import sys


if sys.argv[1] in ['runserver', 'makemigrations', 'migrate', 'createsuperuser']:
    from dotenv import load_dotenv
    load_dotenv()

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    sys.exit(
        """
        В файле .env необходим параметр DJANGO_SETTINGS_MODULE со
        значением 'config.settings.develop' или 'config.settings.product'
        """
    )


def main():
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        os.getenv('DJANGO_SETTINGS_MODULE')
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
