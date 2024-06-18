from rest_framework import serializers

from tags.models import Tag

from api.utils.variables import (
    VALIDATE_MSG_COMMON,
    VALIDATE_MSG_EXIST_TAG,
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id', 'name', 'slug',

    def to_internal_value(self, data):
        if not isinstance(data, int):
            raise serializers.ValidationError(VALIDATE_MSG_COMMON)
        if not self.Meta.model.objects.filter(id=data).exists():
            raise serializers.ValidationError(VALIDATE_MSG_EXIST_TAG)
        return self.Meta.model.objects.get(id=data)
