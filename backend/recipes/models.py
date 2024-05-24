from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from recipes.variables import ALLOWED_LEN_NAME, MINIMUM_TIME_COOKING


class Tag(models.Model):
    name = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Тег',
    )
    slug = models.SlugField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Слаг тега',
    )

    class Meta:
        #orderind = []
        #index = [models.Index(fields=[<name_field>])]
        ...

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Единица измерения',
    )


    class Meta:
        ...
        #orderind = []
        #index = [models.Index(fields=[<name_field>])]

    def __str__(self):
        return self.name

class Recipe(models.Model):
    class Presentation(models.IntegerChoices):
        SHOW = 1
        NOT_SHOW = 0

    tags = models.ForeignKey(
        to=Tag,
        on_delete=models.PROTECT,
        verbose_name='Тег',
        related_name='recipes',
    )
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',
    )
    ingredients = models.ForeignKey(
        to=Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ингредиенты',
        related_name='recipes',
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
        ...
        #orderind = []
        #index = [models.Index(fields=[<name_field>])]
    
    def __str__(self):
        return self.name