import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def on_or_off(value: str) -> bool:
    """
    Use human variable for True or False.
    True, true, On, on, Yes, yes --> return True.
    Everything else --> return False.
    """
    return value in ['True', 'true', 'On', 'on', 'Yes', 'yes']


def db(name_db: str = 'default') -> dict:
    """Use need database from permissible."""
    data_base = {
        'postgresql': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'django'),
            'USER': os.getenv('POSTGRES_USER', 'django'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', ''),
            'PORT': os.getenv('DB_PORT', 5432)
        },
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    try:
        return data_base[name_db]
    except KeyError:
        sys.exit('Not correct name database')