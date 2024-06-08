from django.contrib import admin

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Statistic,
    Tag,
)


class RecipeIngredientAmountInline(admin.TabularInline):
    model = RecipeIngredient
    fields = ('recipe', 'ingredient', 'amount')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'show_popularity')
    search_fields = ('name', 'author')
    filter_horizontal = ('tags',)
    inlines = (RecipeIngredientAmountInline,)
    exclude = ('ingredients',)

    def show_popularity(self, obj):
        if Statistic.objects.filter(recipe=obj).exists():
            return Statistic.objects.get(recipe=obj).popularity
        return 0

    show_popularity.short_description = 'Количество добавление в избранное'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
