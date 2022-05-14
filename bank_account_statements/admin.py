from django.contrib import admin
from .models import Bank, Statement

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    pass

@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    pass
