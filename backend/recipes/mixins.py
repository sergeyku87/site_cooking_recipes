from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import redirect, render
from django.urls import path

import csv

from recipes.forms import CsvImportForm


class CommonForM2M(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        to='Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.recipe}'


class CSVMixin():
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('csv-upload/', self.upload_csv),
        ]
        return my_urls + urls

    def upload_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf8').splitlines()
            reader = csv.DictReader(
                decoded_file,
                delimiter=',',
                fieldnames=self.csv_fields,
            )
            for row in reader:
                try:
                    self.model.objects.create(**row)
                except Exception as err:
                    self.message_user(request, f'Ошибка {err}')
                    pass
            return redirect('..')
        form = CsvImportForm()
        payload = {'form': form}
        return render(
            request, 'admin/csv_import.html', payload
        )
