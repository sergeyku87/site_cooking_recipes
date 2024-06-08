from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import serializers

from users.models import Subscription
from users.utils import base64_to_image, representation_image
from users.variables import VALIDATION_MSG_ERROR


class UserGETSerializer(serializers.ModelSerializer):
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
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password')
        )
        return super().create(validated_data)


class CustomImageField(serializers.Field):
    def to_representation(self, value):
        return representation_image(
            self.context.get('request'),
            value.url
        )

    def to_internal_value(self, data):
        prefix_name_image = self.context.get('request').user.username
        return base64_to_image(data, prefix_name_image)


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
        return Subscription.objects.filter(
            user=obj,
            subscriber=self.context.get('request').user,
        ).exists()

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
