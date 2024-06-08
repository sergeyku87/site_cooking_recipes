from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from rest_framework import serializers

from recipes.variables import (
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
        # Replace key 'ingredients_for_recipe' on 'ingredients'
        if attrs and attrs.get('ingredients_for_recipe'):
            ingredients = attrs.pop('ingredients_for_recipe')
            attrs.update(ingredients=ingredients)
        return super().validate(attrs)
