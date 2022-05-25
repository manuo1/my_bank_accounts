from django.contrib import admin

from categorization.models import Category, CategoryKeyword


@admin.register(CategoryKeyword)
class CategoryKeywordAdmin(admin.ModelAdmin):
    search_fields = ["keyword", "category__name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
