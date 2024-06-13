import os

from django.core.wsgi import get_wsgi_application

from base.config import DEVELOP


if DEVELOP:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.develop')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.product')

application = get_wsgi_application()
