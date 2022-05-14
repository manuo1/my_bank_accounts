from django import forms

from .models import Statement


class SatementForm(forms.ModelForm):
    class Meta:
        model = Statement
        fields = ('name', 'bank', 'file')