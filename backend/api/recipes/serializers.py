from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import serializers, validators

from api.recipes.fields import CustomImageField
from api.mixins import ValidateRecipeMixin
from api.tags.serializers import TagSerializer
from api.users.serializers import UserGETSerializer
from api.utils.variables import (
    ERROR_RESPONSE_CART,
    ERROR_RESPONSE_FAVORITE,
    VALIDATE_MSG_COUNT_INGREDIENT,
    VALIDATE_MSG_EXIST_INGREDIENT,
    VALIDATE_MSG_UNIQUE,
)
from api.utils.utils import representation_image
from ingredients.models import Ingredient
from recipes.models import Favorite, Recipe, RecipeIngredient, ShoppingCart


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


class RecipeSerializer(ValidateRecipeMixin, serializers.ModelSerializer):
    author = UserGETSerializer(read_only=True)
    tags = TagSerializer(many=True, required=True)
    image = CustomImageField()
    is_favorited = serializers.SerializerMethodField('get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_is_in_shopping_cart'
    )
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
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.set(tags)
        instance.ingredients.clear()

        for value in ingredients:
            instance.ingredients.add(
                value['ingredient'],
                through_defaults={'amount': value['amount']}
            )

        super().update(instance, validated_data)
        return instance

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            user = self.context.get('request').user
            return obj.shopping_cart.filter(
                user=user,
                recipe=obj,
            ).exists()
        return False

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return obj.favorite.filter(
            user=request.user,
            recipe=obj,
        ).exists() if request.user.is_authenticated else False


class RecipeShortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = serializers.CharField()
    cooking_time = serializers.IntegerField()

    def to_representation(self, instance):
        instance.image = representation_image(
            self.context.get('request'),
            instance.image.url
        )
        return super().to_representation(instance)


class CartSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

    def validate_pk(self, obj):
        return get_object_or_404(Recipe, id=obj)

    def create(self, validated_data):
        instance, created = ShoppingCart.objects.get_or_create(
            user=self.context.get('request').user,
            recipe=validated_data.get('pk'),
        )
        if not created:
            raise serializers.ValidationError(ERROR_RESPONSE_CART)
        return instance.recipe

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class FavoriteSerializer(CartSerializer):
    def create(self, validated_data):
        instance, created = Favorite.objects.get_or_create(
            user=self.context.get('request').user,
            recipe=validated_data.get('pk'),
        )
        if not created:
            raise serializers.ValidationError(ERROR_RESPONSE_FAVORITE)
        return instance.recipe

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
