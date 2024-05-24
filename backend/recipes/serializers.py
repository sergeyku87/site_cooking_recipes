from rest_framework import serializers

from recipes.models import  Ingredient, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fieds = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fieds = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fieds = '__all__'
