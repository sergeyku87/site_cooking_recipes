from django import forms
from django.forms.models import BaseInlineFormSet

from common.variables import VALIDATE_MSG_INGREDIENT


class RicepeIngredientForm(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if hasattr(self, 'cleaned_data'):
            data = [bool(value) for value in self.cleaned_data]
            if not any(data):
                raise forms.ValidationError(
                    VALIDATE_MSG_INGREDIENT
                )
