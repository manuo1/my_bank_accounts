from django.contrib import admin

from current_month.models import BankWebSiteData, TransactionWithoutStatement

admin.site.register(TransactionWithoutStatement)
admin.site.register(BankWebSiteData)
