from django.contrib import admin

from common.mixins import CSVMixin
from tags.models import Tag


@admin.register(Tag)
class TagAdmin(CSVMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    csv_fields = ('name', 'slug')
