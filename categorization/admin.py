from django.contrib import admin

from categorization.models import Category, CategoryKeyword

admin.site.register(Category)


@admin.register(CategoryKeyword)
class CategoryKeywordAdmin(admin.ModelAdmin):
    ordering = ["keyword"]
    search_fields = ["keyword", "category__name"]
