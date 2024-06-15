from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

import pdfkit
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from shortener import shortener

from api.recipes.filters import RecipeFilter
from api.recipes.paginations import PageLimitPagination
from api.recipes.permissions import IsOwner
from api.recipes.serializers import (
    CartOrFavoriteSerializer,
    RecipeSerializer,
)
from api.fixtures.utils import delete_or_400
from api.fixtures.variables import (
    ERROR_RESPONSE_CART,
    ERROR_RESPONSE_FAVORITE,
    FORMAT_FULL_LINK,
    FORMAT_SHORT_LINK,
    PERMISSION_IS_AUTH,
    PERMISSION_IS_OWNER,
)
from recipes.models import (
    Favorite,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
)


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
            if not (
                ingredient.ingredient.name,
                ingredient.ingredient.measurement_unit
            ) in ingredients_for_buy:
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

        template = get_template('pdf.html')
        html = template.render({'buy': ingredients_for_buy})
        pdf = pdfkit.from_string(html, False)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=output.pdf'
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
