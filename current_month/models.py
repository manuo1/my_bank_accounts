from django.db import models
from django.db.models.signals import post_save
from categorization.models import Category
from current_month.mutators import create_transactions_with_bank_web_site_data


class BankWebSiteData(models.Model):
    data = models.TextField()

    def save(self, *args, **kwargs):
        BankWebSiteData.objects.all().delete()
        super().save(*args, **kwargs)


def bank_web_site_data_post_save(sender, instance, created, *args, **kwargs):
    if created:
        create_transactions_with_bank_web_site_data()


post_save.connect(bank_web_site_data_post_save, sender=BankWebSiteData)
