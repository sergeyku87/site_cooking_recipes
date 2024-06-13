import os

from django.core.asgi import get_asgi_application

from base.config import DEVELOP


if DEVELOP:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.develop')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.product')

application = get_asgi_application()
