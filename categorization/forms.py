from django import forms

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
