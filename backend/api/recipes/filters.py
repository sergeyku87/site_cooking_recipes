import django_filters

from ingredients.models import Ingredient
from recipes.models import Recipe
from tags.models import Tag


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = []


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        to_field_name='slug',
        field_name='tags__slug',
    )
    is_favorited = django_filters.NumberFilter(method='filter_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(method='filter_cart')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def filter_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            id_favorited = []
            for recipe in queryset:
                if recipe.favorite.filter(
                    user=user,
                    recipe=recipe
                ).exists():
                    id_favorited.append(recipe.id)
            return queryset.filter(id__in=id_favorited)
        return queryset

    def filter_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            id_shoping_cart = []
            for recipe in queryset:
                if recipe.shopping_cart.filter(
                    user=user,
                    recipe=recipe
                ).exists():
                    id_shoping_cart.append(recipe.id)
            return queryset.filter(id__in=id_shoping_cart)
        return queryset
