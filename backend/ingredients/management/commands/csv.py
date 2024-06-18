from django.core.management.base import BaseCommand

import csv
import logging
from pathlib import Path

from ingredients.models import Ingredient


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(name)s-%(asctime)s-%(levelname)s-%(message)s'
)
logger.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)


class Command(BaseCommand):
    """
    Command for fill table Ingredient.
    Example:
        manage.py csv data/file.csv
        manage.py csv ../data/file.csv
    """

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            path = Path.cwd()
            tail = options.get('path')[0]
            if tail.startswith('..'):
                path = path.parent
                tail = tail[3:]
            full_path = path / tail
            if full_path.exists() and full_path.is_file():
                fieldnames = ['name', 'measurement_unit']
                with open(full_path, 'r', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(
                        file,
                        delimiter=',',
                        fieldnames=fieldnames
                    )
                    ingredients = (Ingredient(**row) for row in csv_reader)
                    Ingredient.objects.bulk_create(ingredients)
                    return 'successfully'
        except Exception as exc:
            logger.error(exc)
