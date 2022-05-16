from django.contrib import admin
from .models import Bank, Statement, Transaction

admin.site.register(Bank)

admin.site.register(Statement)

admin.site.register(Transaction)
