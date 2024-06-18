from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import serializers

from api.utils.variables import (
    REQUIRED_FIELDS_FOR_PATCH,
    VALIDATE_MSG_IMAGE,
    VALIDATE_MSG_INGREDIENT,
    VALIDATE_MSG_TAG,
    VALIDATE_MSG_UNIQUE_INGREDIENT,
    VALIDATE_MSG_UNIQUE_TAG,
)
from users.models import Subscription


class ValidateRecipeMixin:
    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(VALIDATE_MSG_TAG)
        if len(set(value)) != len(value):
            raise serializers.ValidationError(VALIDATE_MSG_UNIQUE_TAG)
        return value

    def validate_ingredients(self, value):
        ingredients = [val['ingredient'] for val in value]
        if len(set(ingredients)) != len(ingredients):
            raise serializers.ValidationError(VALIDATE_MSG_UNIQUE_INGREDIENT)
        if not value:
            raise serializers.ValidationError(VALIDATE_MSG_INGREDIENT)
        return value

    def validate_image(self, value):
        if not isinstance(value, InMemoryUploadedFile):
            raise serializers.ValidationError(VALIDATE_MSG_IMAGE)
        return value

    def validate(self, attrs):
        if self.partial:
            for need_field in REQUIRED_FIELDS_FOR_PATCH:
                if need_field not in self.initial_data:
                    raise serializers.ValidationError(
                        f'Отсутствует {need_field}'
                    )
        # Replace key 'ingredients_for_recipe' on 'ingredients'
        if attrs and attrs.get('ingredients_for_recipe'):
            ingredients = attrs.pop('ingredients_for_recipe')
            attrs.update(ingredients=ingredients)
        return super().validate(attrs)


class CommonMethodMixin:
    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=obj,
            subscriber=self.context.get('request').user,
        ).exists() if (
            self.context.get('request').user.is_authenticated
        ) else False
