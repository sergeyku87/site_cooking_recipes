from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from users.utils import base64_to_image


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
        request = self.context.get('request')
        host = request.META['HTTP_HOST']
        protocol = 'http'
        return f'{protocol}://{host}{value.url}'

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