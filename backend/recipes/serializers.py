from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers, validators

from recipes.models import  Ingredient, Recipe, RecipeIngredient, Tag
from recipes.utils import base64_to_image, debug


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        )


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Tag
        fields = 'id', 'name', 'slug',

    def to_internal_value(self, data):
        if not isinstance(data, int):
            self.fail('Not correct value')
        else:
            data = get_object_or_404(
                self.Meta.model,
                id=data,
            )
        return data


class CustomIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = 'id', 'name', 'measurement_unit', 'amount'

    def to_internal_value(self, data):
        id_ingredient = data.pop('id')
        ingredient = get_object_or_404(
            Ingredient,
            id=id_ingredient,
        )
        data.update(ingredient=ingredient)
        return data


class CustomImageField(serializers.ImageField):
    def to_internal_value(self, data):
        name_image = self.parent.initial_data.get('name')
        return base64_to_image(data, name_image=name_image)


class RecipeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, required=True)
    image = CustomImageField()
    ingredients = CustomIngredientSerializer(
        many=True,
        source='ingredients_for_recipe',
        required=True,
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('text', 'name'),
                message="Такой рецепт с таким описанием уже есть."
            )
        ]

    def create(self, validated_data):
        user = self.context.get('request').user
        ingredients_list = validated_data.pop('ingredients')
        tags_list = validated_data.pop('tags')

        with transaction.atomic():
            recipe = Recipe(**validated_data, author=user)
            recipe.save()
            recipe.tags.set(tags_list)

            for value in ingredients_list:
                recipe.ingredients.add(
                    value['ingredient'],
                    through_defaults={'amount': value['amount']}
                )
            return recipe
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if hasattr(instance, key):
                if getattr(instance, key).__class__.__name__ == 'ManyRelatedManager':
                    if key == 'tags':
                        getattr(instance, key).set(value)
                    elif key == 'ingredients':
                        for val in value:
                            getattr(instance, 'ingredients').add(
                                val['ingredient'],
                                through_defaults={'amount': val['amount']}
                            )
                else:
                    setattr(instance, key, value)
        instance.save()
        return instance
    
    def validate(self, attrs):
        # Replace key 'ingredients_for_recipe' on 'ingredients'
        ingredients = attrs.pop('ingredients_for_recipe')
        attrs.update(ingredients=ingredients)
        return super().validate(attrs)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'