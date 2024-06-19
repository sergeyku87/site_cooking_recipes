from django.core.management.utils import get_random_secret_key

import os

# from config.settings.base_settings import *


SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

DEBUG = False

ALLOWED_HOSTS = [
    os.getenv('ALLOWED_HOST', '*'),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'django'),
        'USER': os.getenv('POSTGRES_USER', 'django'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', 5432)
    }
}

MEDIA_ROOT = '/media/'
