from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from recipes.variables import ALLOWED_LEN_NAME, MINIMUM_TIME_COOKING


class Tag(models.Model):
    name = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Тег',
        #db_index=True
    )
    slug = models.SlugField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Слаг тега',
        unique=True,
        #db_index=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        #orderind = []
        #index = [models.Index(fields=[<name_field>])]
        

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Название ингредиента',
        unique=True,
    )
    measurement_unit = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Единица измерения',
    )


    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        #orderind = []
        #index = [models.Index(fields=[<name_field>])]

    def __str__(self):
        return self.name

class Recipe(models.Model):
    class Presentation(models.IntegerChoices):
        SHOW = 1, 'Да'
        NOT_SHOW = 0, 'Нет'

    tags = models.ManyToManyField(
        to='Tag',
        verbose_name='Тег',
        blank=True,
        #related_name='',
    )
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        to='Ingredient',
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
        related_name='recipes',
        blank=True,
    )
    is_favorited = models.BooleanField(
        choices=Presentation.choices,
        default=Presentation.SHOW,
        verbose_name='Показывать рецепты из избранного',
    )
    is_in_shopping_cart = models.BooleanField(
        choices=Presentation.choices,
        default=Presentation.SHOW,
        verbose_name='Показывать  рецепты из списка покупок',
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

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        #orderind = []
        #index = [models.Index(fields=[<name_field>])]
    
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
