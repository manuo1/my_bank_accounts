from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Statement


class SatementForm(forms.ModelForm):
    class Meta:
        model = Statement
        fields = ("file", "bank")
        labels = {
            "file": "Fichier PDF",
            "bank": "Choix de la Banque",
        }
        widgets = {
            "bank": forms.RadioSelect,
            "file": forms.ClearableFileInput,
        }
