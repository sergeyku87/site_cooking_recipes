from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_init
from django.dispatch import receiver

from recipes.mixins import CommonForM2M
from recipes.variables import ALLOWED_LEN_NAME, MINIMUM_TIME_COOKING


class Tag(models.Model):
    name = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Тег',
        unique=True,
    )
    slug = models.SlugField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Слаг тега',
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


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


class Recipe(models.Model):
    class Status(models.IntegerChoices):
        ADDED = 1, 'Да'
        NOT_ADDED = 0, 'Нет'

    tags = models.ManyToManyField(
        to='Tag',
        verbose_name='Тег',
        blank=True,
    )
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes_user',
    )
    ingredients = models.ManyToManyField(
        to='Ingredient',
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
        related_name='recipes',
        blank=True,
    )
    is_favorited = models.BooleanField(
        choices=Status.choices,
        default=Status.NOT_ADDED,
        verbose_name='Рецепт в избранном',
    )
    is_in_shopping_cart = models.BooleanField(
        choices=Status.choices,
        default=Status.NOT_ADDED,
        verbose_name='Рецепт в список покупок',
    )
    name = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='photos_recipes/%Y/%m/%d/',
        verbose_name='Фото рецепта',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MINIMUM_TIME_COOKING)],
        verbose_name='Время приготовления (минуты)'
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Время изменения',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        to='Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredients_for_recipe'
    )
    ingredient = models.ForeignKey(
        to='Ingredient',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингредиент и его количество'
        verbose_name_plural = 'Ингредиенты и их количество'

    def __str__(self):
        return f'{self.ingredient.name} {self.ingredient.measurement_unit}'


class ShoppingCart(CommonForM2M):
    class Meta:
        verbose_name = 'Корзина товаров'
        verbose_name_plural = 'Корзина товаров'
        default_related_name = 'shopping_cart'
        unique_together = ('user', 'recipe')


class Favorite(CommonForM2M):
    class Meta:
        verbose_name = 'Рецепт в избранном'
        verbose_name_plural = 'Рецепты в избранном'
        default_related_name = 'favorite'
        unique_together = ('user', 'recipe')


class Statistic(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
    )
    popularity = models.IntegerField(default=1)


@receiver(pre_init, sender=Favorite)
def increment_popularity(sender, **kwargs):
    if kwargs.get('kwargs'):
        recipe = kwargs.get('kwargs').get('recipe')
        instance, created = Statistic.objects.get_or_create(
            recipe=recipe,
        )
        if not created:
            instance.popularity += 1
            instance.save()
