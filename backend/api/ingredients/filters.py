import django_filters

from ingredients.models import Ingredient


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = []
