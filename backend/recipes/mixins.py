from django.contrib.auth import get_user_model
from django.db import models


class CommonForM2M(models.Model):
    """
    Abstract model for extend models with relation ManyToManyField.
    """
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
