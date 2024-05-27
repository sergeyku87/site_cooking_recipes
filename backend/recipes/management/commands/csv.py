from django.core.management.base import BaseCommand

import csv
from pathlib import Path

from recipes.models import Ingredient


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
        path = Path.cwd()
        tail = options.get('path')[0]
        if tail.startswith('..'):
            path = path.parent
        full_path = path / tail[3:]
        if full_path.exists() and full_path.is_file():
            fieldnames = ['name', 'measurement_unit']
            with open(full_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file, delimiter = ",", fieldnames=fieldnames)
                for row in csv_reader:
                    Ingredient.objects.create(
                        name=row['name'],
                        measurement_unit=row['measurement_unit']
                    )
                return 'successfully'