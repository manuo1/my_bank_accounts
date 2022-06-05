from django import forms

from current_month.models import BankWebSiteData


class BankWebSiteDataForm(forms.ModelForm):
    class Meta:
        model = BankWebSiteData
        fields = ("data",)
        labels = {
            "data": "Données de la banque",
        }
