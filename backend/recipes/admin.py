from django.contrib import admin

from recipes.forms import RicepeIngredientForm
from recipes.models import (
    Favorite,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Statistic,
)


class RecipeIngredientAmountInline(admin.TabularInline):
    model = RecipeIngredient
    fields = ('recipe', 'ingredient', 'amount')
    formset = RicepeIngredientForm


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'show_popularity')
    search_fields = ('name', 'author')
    filter_horizontal = ('tags',)
    inlines = (RecipeIngredientAmountInline,)

    @admin.display(description='Количество добавление в избранное')
    def show_popularity(self, obj):
        if Statistic.objects.filter(recipe=obj).exists():
            return Statistic.objects.get(recipe=obj).popularity
        return 0


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
