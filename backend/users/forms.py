from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from users.models import Subscription
from users.utils import validate_fields
from users.variables import (
    ERROR_MSG_SUBSCRIBE,
    ERROR_MSG_SUBSCRIBE_CREATE,
    VALIDATION_MSG_NAME,
)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password',
            'password2',
            'username',
            'first_name',
            'last_name'
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def clean(self):
        data = self.cleaned_data
        result, value = validate_fields(
            '^me',
            [data.get('username'), data.get('first_name')]
        )
        if result:
            raise ValidationError(VALIDATION_MSG_NAME.format(value))
        return data


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'is_active', )


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'

    def clean(self):
        data = self.cleaned_data
        if data.get('user') == data.get('subscriber'):
            raise forms.ValidationError(ERROR_MSG_SUBSCRIBE)
        elif Subscription.objects.filter(
            user=data.get('user'),
            subscriber=data.get('subscriber'),
        ).exists():
            raise forms.ValidationError(ERROR_MSG_SUBSCRIBE_CREATE)
        return data
