from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from io import StringIO
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from shortener import shortener

from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from recipes.paginations import PageLimitPagination
from recipes.permissions import IsOwner
from recipes.serializers import (
    CartOrFavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from recipes.utils import delete_or_400
from recipes.variables import (
    ERROR_RESPONSE_CART,
    ERROR_RESPONSE_FAVORITE,
    FORMAT_FILE_DOWNLOAD,
    FORMAT_FULL_LINK,
    FORMAT_SHORT_LINK,
    PERMISSION_IS_AUTH,
    PERMISSION_IS_OWNER,
)


class IngredientViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter
    filter_backends = (DjangoFilterBackend,)


class TagViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = []


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.prefetch_related(
        'ingredients',
        'tags',
    ).select_related(
        'author'
    ).order_by('-time_create')
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)

    @action(['get'], detail=True, url_path='get-link')
    def get_link(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get('pk'))
        link = request.get_full_path().replace(
            'get-link/', ''
        ).replace('/api/', '')
        user = recipe.author
        full_link = FORMAT_FULL_LINK.format(
            request.scheme,
            request.get_host(),
            link,
        )
        if user.urlmap_set.filter(full_url=link).exists():
            short_link = user.urlmap_set.get(full_url=full_link).short_url
        short_link = shortener.create(recipe.author, full_link)

        return Response(
            {
                'short-link': FORMAT_SHORT_LINK.format(
                    request.scheme,
                    request.get_host(),
                    short_link,
                )
            }
        )

    @action(['get'], detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        cart = ShoppingCart.objects.filter(
            user=request.user.id
        ).values_list('recipe__id', flat=True)
        ingredients = RecipeIngredient.objects.filter(recipe_id__in=cart)
        ingredients_for_buy = {}

        for ingredient in ingredients:
            if ingredient.ingredient.name not in ingredients_for_buy:
                ingredients_for_buy[
                    (
                        ingredient.ingredient.name,
                        ingredient.ingredient.measurement_unit
                    )
                ] = ingredient.amount
            else:
                ingredients_for_buy[
                    (
                        ingredient.ingredient.name,
                        ingredient.ingredient.measurement_unit
                    )
                ] += ingredient.amount

        with StringIO() as buffer:
            for ingredient, amount in ingredients_for_buy.items():
                buffer.write(
                    FORMAT_FILE_DOWNLOAD.format(
                        ingredient[0],
                        amount,
                        ingredient[1],
                    )
                )
            response = HttpResponse(
                buffer.getvalue(),
                content_type='text/plain'
            )
            response['Content-Disposition'] = (
                'attachment; filename="list-for-buy.txt"'
            )
            return response

    @action(['post', 'delete'], detail=True, url_path='shopping_cart')
    def shopping_cart(self, request, *args, **kwargs):
        if request.method == 'POST' or request.method == 'DELETE':
            recipe = get_object_or_404(
                Recipe,
                id=kwargs.get('pk')
            )
        if request.method == 'POST':
            _, created = ShoppingCart.objects.get_or_create(
                user=request.user,
                recipe=recipe,
            )
            if not created:
                return Response(
                    {'error': ERROR_RESPONSE_CART},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'DELETE':
            return delete_or_400(
                ShoppingCart,
                user=request.user,
                recipe=recipe,
            )

        serializer = CartOrFavoriteSerializer(
            recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(['post', 'delete'], detail=True,)
    def favorite(self, request, *args, **kwargs):
        if request.method == 'POST' or request.method == 'DELETE':
            recipe = get_object_or_404(
                Recipe,
                id=kwargs.get('pk')
            )
        if request.method == 'POST':
            _, created = Favorite.objects.get_or_create(
                user=request.user,
                recipe=recipe,
            )
            if not created:
                return Response(
                    {'error': ERROR_RESPONSE_FAVORITE},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'DELETE':
            return delete_or_400(
                Favorite,
                user=request.user,
                recipe=recipe,
            )

        serializer = CartOrFavoriteSerializer(
            recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action in PERMISSION_IS_AUTH:
            permission_classes = [IsAuthenticated]
        elif self.action in PERMISSION_IS_OWNER:
            permission_classes = [IsOwner]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
