from django.db import models
from django.db.models.signals import post_save
from categorization.models import Category
from current_month.mutators import create_transactions_with_bank_web_site_data


class TransactionWithoutStatement(models.Model):
    date = models.DateField()
    label = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=20, decimal_places=2)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL
    )
    extended_label = models.CharField(max_length=255, blank=True)
    custom_label = models.CharField(max_length=255, blank=True)
    fitid = models.CharField(max_length=255)


class BankWebSiteData(models.Model):
    data = models.TextField()

    def save(self, *args, **kwargs):
        BankWebSiteData.objects.all().delete()
        super().save(*args, **kwargs)


def bank_web_site_data_post_save(sender, instance, created, *args, **kwargs):
    if created:
        create_transactions_with_bank_web_site_data()


post_save.connect(bank_web_site_data_post_save, sender=BankWebSiteData)
