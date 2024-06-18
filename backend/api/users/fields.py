from rest_framework import serializers

from common.utils import base64_to_image, representation_image


class CustomImageField(serializers.Field):
    def to_representation(self, value):
        return representation_image(
            self.context.get('request'),
            value.url
        )

    def to_internal_value(self, data):
        prefix_name_image = self.context.get('request').user.username
        return base64_to_image(data, prefix_name_image)
