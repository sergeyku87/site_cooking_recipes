from django.core.wsgi import get_wsgi_application

import os


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    os.getenv('DJANGO_SETTINGS_MODULE')
)

application = get_wsgi_application()
