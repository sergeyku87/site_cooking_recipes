from django.contrib import admin

from recipes.models import  Ingredient, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ...


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ...