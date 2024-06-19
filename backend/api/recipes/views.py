from django.db.models import Sum
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
from api.paginations import PageLimitPagination
from api.permissions import IsOwner
from api.recipes.serializers import (
    CartSerializer,
    FavoriteSerializer,
    RecipeSerializer,
)
from api.utils.variables import (
    FORMAT_FULL_LINK,
    FORMAT_SHORT_LINK,
    PERMISSION_IS_AUTH,
    PERMISSION_IS_OWNER,
)
from api.utils.utils import delete_or_400
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
        result = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user,
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(total=Sum('amount'))

        template = get_template('pdf.html')
        html = template.render(
            {'buy': result}
        )
        pdf = pdfkit.from_string(html, False)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=output.pdf'
        return response

    @action(['post'], detail=True, url_path='shopping_cart')
    def shopping_cart(self, request, *args, **kwargs):
        serializer = CartSerializer(
            data=kwargs,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, *args, **kwargs):
        recipe = get_object_or_404(
            Recipe,
            id=kwargs.get('pk')
        )
        return delete_or_400(
            ShoppingCart,
            user=request.user,
            recipe=recipe,
        )

    @action(['post'], detail=True,)
    def favorite(self, request, *args, **kwargs):
        serializer = FavoriteSerializer(
            data=kwargs,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, *args, **kwargs):
        recipe = get_object_or_404(
            Recipe,
            id=kwargs.get('pk')
        )
        return delete_or_400(
            Favorite,
            user=request.user,
            recipe=recipe,
        )

    def get_permissions(self):
        if self.action in PERMISSION_IS_AUTH:
            permission_classes = [IsAuthenticated]
        elif self.action in PERMISSION_IS_OWNER:
            permission_classes = [IsOwner]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
