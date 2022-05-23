from django.contrib import admin
from .models import Bank, Statement, Transaction

admin.site.register(Bank)

admin.site.register(Statement)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    ordering = ["date"]
    search_fields = ["extended_label"]
