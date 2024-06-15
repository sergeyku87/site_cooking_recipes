from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet


from tags.models import Tag
from api.tags.serializers import TagSerializer


class TagViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = []
