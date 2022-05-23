from django import forms
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
