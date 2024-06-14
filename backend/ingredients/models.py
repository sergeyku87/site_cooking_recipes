from django.db import models

from ingredients.variables import ALLOWED_LEN_NAME


class Ingredient(models.Model):
    name = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Название ингредиента',
        unique=True,
        db_index=True,
    )
    measurement_unit = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
