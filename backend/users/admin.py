from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.forms import SubscriptionForm, UserChangeForm, UserCreationForm
from users.models import Subscription


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'username', 'email', )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email',)
    ordering = ('email',)
    filter_horizontal = ()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionForm
    list_display = ('user', 'subscriber')
