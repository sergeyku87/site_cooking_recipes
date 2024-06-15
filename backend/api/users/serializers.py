from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.users.fields import CustomImageField
from api.fixtures.utils import representation_image, validate_fields
from api.fixtures.variables import (
    VALIDATION_MSG_ERROR,
    VALIDATION_MSG_NAME,
)
from users.models import Subscription


class UserGETSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

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
        if self.context.get('request').user.is_authenticated:
            return Subscription.objects.filter(
                user=obj,
                subscriber=self.context.get('request').user,
            ).exists()
        return False


class UserPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'validators': [validate_password],
            },
            'username': {
                'validators': [
                    UniqueValidator(
                        get_user_model().objects,
                        'Not unique',
                    )
                ]
            },
            'email': {
                'validators': [
                    UniqueValidator(
                        get_user_model().objects,
                        'Not unique',
                    )
                ]
            },
        }

    def validate(self, attrs):
        result, value = validate_fields(
            '^me',
            [attrs.get('username'), attrs.get('first_name')]
        )
        if result:
            raise serializers.ValidationError(
                VALIDATION_MSG_NAME.format(value)
            )
        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password')
        )
        return super().create(validated_data)


class AvatarSerializer(serializers.Serializer):
    avatar = CustomImageField()

    class Meta:
        model = get_user_model()
        fields = ('avatar',)

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance

    def validate_avatar(self, value):
        if not isinstance(value, InMemoryUploadedFile):
            raise serializers.ValidationError(VALIDATION_MSG_ERROR)
        return value


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


class SubscribeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    recipes = serializers.SerializerMethodField('get_recipes')
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')
    avatar = serializers.ImageField()

    def get_recipes_count(self, obj):
        return obj.recipes_user.count()

    def get_is_subscribed(self, obj):
        if self.context.get('request').user.is_authenticated:
            return Subscription.objects.filter(
                user=obj,
                subscriber=self.context.get('request').user,
            ).exists()
        return False

    def get_recipes(self, obj):
        request = self.context.get('request')
        queryset = obj.recipes_user.all()
        if request.query_params.get('recipes_limit'):
            limit = int(request.query_params.get('recipes_limit'))
            queryset = queryset[:limit]
        return RecipeShortSerializer(
            queryset,
            many=True,
            context={'request': request}
        ).data
