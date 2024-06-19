from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.mixins import CommonMethodMixin

from api.users.fields import CustomImageField
from api.utils.variables import (
    ERROR_MSG_SUBSCRIBE,
    ERROR_MSG_SUBSCRIBE_CREATE,
    VALIDATION_MSG_ERROR,
)
from api.utils.utils import specific_validate
from users.models import Subscription


class UserGETSerializer(CommonMethodMixin, serializers.ModelSerializer):
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
            },
        }
        validators = [
            UniqueTogetherValidator(
                queryset=get_user_model().objects.all(),
                fields=['email', 'username']
            )
        ]

    def validate(self, attrs):
        return specific_validate(attrs, serializers.ValidationError)

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


class SubscribeSerializer(CommonMethodMixin, serializers.Serializer):
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

    def get_recipes(self, obj):
        from api.recipes.serializers import RecipeShortSerializer
        # для избежания циклического импорта
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


class SubSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_id(self, obj):
        user_id = self.context.get('request').user.id
        if user_id == obj:
            raise serializers.ValidationError(ERROR_MSG_SUBSCRIBE)
        return get_object_or_404(
            get_user_model(),
            id=obj,
        )

    def create(self, validated_data):
        print(validated_data)
        instance, created = Subscription.objects.get_or_create(
            user=self.context.get('request').user,
            subscriber=validated_data.get('id'),
        )
        if not created:
            raise serializers.ValidationError(ERROR_MSG_SUBSCRIBE_CREATE)
        return instance.subscriber

    def to_representation(self, instance):
        return SubscribeSerializer(
            instance,
            context={'request': self.context.get('request')},
        ).data
