from django import forms
from bank_account_statements.models import Transaction

from categorization.models import Category, CategoryKeyword


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        labels = {
            "name": "Nom",
        }


class CategoryKeywordForm(forms.ModelForm):
    class Meta:
        model = CategoryKeyword
        fields = ("keyword", "category")
        labels = {
            "keyword": "Mot clé",
            "category": "Catégorie",
        }


class TransactionCustomLabelForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("custom_label",)
        labels = {
            "custom_label": "Libellé personnalisé",
        }
