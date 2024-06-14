from django.contrib import admin

from ingredients.mixins import CSVMixin
from ingredients.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(CSVMixin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    csv_fields = ('name', 'measurement_unit')
