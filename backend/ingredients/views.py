from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from ingredients.filters import IngredientFilter
from ingredients.models import Ingredient
from api.ingredients.serializers import IngredientSerializer


class IngredientViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter
    filter_backends = (DjangoFilterBackend,)
