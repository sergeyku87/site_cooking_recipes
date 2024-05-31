from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from recipes.models import Ingredient, Recipe, Tag
from recipes.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)

class IngredientViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    
    @action(['get'], detail=True, url_path='get-link')
    def get_link(self, request, *args, **kwargs):
        return Response({'plug': 'Plug'})
    
    @action(['get'], detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        return Response({'plug': 'Plug'})
    
    @action(['post', 'delete'], detail=True, url_path='shopping_cart')
    def shopping_cart(self, request, *args, **kwargs):
        return Response({'plug': 'Plug'})

    @action(['post', 'delete'], detail=True,)
    def favorite(self, request, *args, **kwargs):
        return Response({'plug': 'Plug'})

