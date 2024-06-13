from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.shortcuts import redirect, render
from django.urls import path

import csv
from rest_framework import serializers

from recipes.forms import CsvImportForm
from recipes.variables import (
    REQUIRED_FIELDS_FOR_PATCH,
    VALIDATE_MSG_IMAGE,
    VALIDATE_MSG_INGREDIENT,
    VALIDATE_MSG_TAG,
    VALIDATE_MSG_UNIQUE_INGREDIENT,
    VALIDATE_MSG_UNIQUE_TAG,
)


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


class ValidateRecipeMixin:
    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(VALIDATE_MSG_TAG)
        if len(set(value)) != len(value):
            raise serializers.ValidationError(VALIDATE_MSG_UNIQUE_TAG)
        return value

    def validate_ingredients(self, value):
        ingredients = [val['ingredient'] for val in value]
        if len(set(ingredients)) != len(ingredients):
            raise serializers.ValidationError(VALIDATE_MSG_UNIQUE_INGREDIENT)
        if not value:
            raise serializers.ValidationError(VALIDATE_MSG_INGREDIENT)
        return value

    def validate_image(self, value):
        if not isinstance(value, InMemoryUploadedFile):
            raise serializers.ValidationError(VALIDATE_MSG_IMAGE)
        return value

    def validate(self, attrs):
        if self.partial:
            for need_field in REQUIRED_FIELDS_FOR_PATCH:
                if need_field not in self.initial_data:
                    raise serializers.ValidationError(
                        f'Отсутствует {need_field}'
                    )
        # Replace key 'ingredients_for_recipe' on 'ingredients'
        if attrs and attrs.get('ingredients_for_recipe'):
            ingredients = attrs.pop('ingredients_for_recipe')
            attrs.update(ingredients=ingredients)
        return super().validate(attrs)


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
