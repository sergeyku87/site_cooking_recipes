from django import forms
from django.forms.models import BaseInlineFormSet

from recipes.variables import VALIDATE_MSG_INGREDIENT


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class RicepeIngredientForm(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if hasattr(self, 'cleaned_data'):
            data = [bool(value) for value in self.cleaned_data]
            if not any(data):
                raise forms.ValidationError(
                    VALIDATE_MSG_INGREDIENT
                )
