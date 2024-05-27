from django.contrib import admin

from recipes.models import  Ingredient, Recipe, Tag, RecipeIngredient

class RecipeIngredientAmountInline(admin.TabularInline):
    model = RecipeIngredient
    fields = ('recipe', 'ingredient', 'amount')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags', )
    inlines = (RecipeIngredientAmountInline,)
    exclude = ('ingredients',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ...