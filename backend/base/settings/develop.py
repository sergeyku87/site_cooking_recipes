from django.core.management.utils import get_random_secret_key

from base.settings.base_settings import BASE_DIR
# from base.settings.base_settings import *


SECRET_KEY = get_random_secret_key()

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_ROOT = BASE_DIR / 'media/'
