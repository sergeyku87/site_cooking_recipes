from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import serializers, validators

from recipes.mixins import ValidateRecipeMixin
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from recipes.utils import base64_to_image, representation_image
from recipes.variables import (
    M2M,
    VALIDATE_MSG_COMMON,
    VALIDATE_MSG_COUNT_INGREDIENT,
    VALIDATE_MSG_EXIST_INGREDIENT,
    VALIDATE_MSG_EXIST_TAG,
    VALIDATE_MSG_INGREDIENT,
    VALIDATE_MSG_UNIQUE,
)
from users.models import Subscription


class AuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
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

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=self.context.get('request').user,
            subscriber=obj,
        ).exists()


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Tag
        fields = 'id', 'name', 'slug',

    def to_internal_value(self, data):
        if not isinstance(data, int):
            raise serializers.ValidationError(VALIDATE_MSG_COMMON)
        if not self.Meta.model.objects.filter(id=data).exists():
            raise serializers.ValidationError(VALIDATE_MSG_EXIST_TAG)

        return self.Meta.model.objects.get(id=data)


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
        if int(data.get('amount')) < 1:
            raise serializers.ValidationError(VALIDATE_MSG_COUNT_INGREDIENT)
        id_ingredient = data.pop('id')
        if not Ingredient.objects.filter(id=id_ingredient).exists():
            raise serializers.ValidationError(VALIDATE_MSG_EXIST_INGREDIENT)
        ingredient = get_object_or_404(
            Ingredient,
            id=id_ingredient,
        )
        data.update(ingredient=ingredient)
        return data


class CustomImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if not data:
            raise serializers.ValidationError(VALIDATE_MSG_INGREDIENT)
        name_image = self.parent.initial_data.get('name', 'default')
        return base64_to_image(data, name_image=name_image)


class RecipeSerializer(ValidateRecipeMixin, serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, required=True)
    image = CustomImageField()
    is_favorited = serializers.BooleanField(required=False)
    is_in_shopping_cart = serializers.BooleanField(required=False)
    ingredients = CustomIngredientSerializer(
        many=True,
        source='ingredients_for_recipe',
        required=True,
    )

    class Meta:
        model = Recipe
        exclude = ('time_create', 'time_update')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('text', 'name'),
                message=VALIDATE_MSG_UNIQUE,
            )
        ]
        extra_kwargs = {
            'name': {'required': True},
        }

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
                if getattr(instance, key).__class__.__name__ == M2M:
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

    def to_representation(self, instance):
        request = self.context.get('request')
        if request.user.is_authenticated:
            user = self.context.get('request').user
            is_favorited = instance.favorite.filter(
                user=user,
                recipe=instance,
            ).exists()
            is_in_shopping_cart = instance.shopping_cart.filter(
                user=user,
                recipe=instance,
            ).exists()
            instance.is_favorited = is_favorited
            instance.is_in_shopping_cart = is_in_shopping_cart
        return super().to_representation(instance)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class CartOrFavoriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = serializers.CharField()
    cooking_time = serializers.IntegerField()

    def to_representation(self, value):
        value.image = representation_image(
            self.context.get('request'),
            value.image.url
        )
        return super().to_representation(value)
