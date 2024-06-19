from rest_framework import serializers

from api.utils.utils import base64_to_image
from api.utils.variables import VALIDATE_MSG_INGREDIENT


class CustomImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if not data:
            raise serializers.ValidationError(VALIDATE_MSG_INGREDIENT)
        name_image = self.parent.initial_data.get('name', 'default')
        return base64_to_image(data, name_image=name_image)
