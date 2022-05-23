from django.db import models
from django.db.models.signals import post_save, post_delete
import bank_account_statements.models
from categorization.mutators import update_transactions_category


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class CategoryKeyword(models.Model):

    keyword = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.keyword} --> {self.category}"


def category_keyword_post_save(sender, instance, created, *args, **kwargs):
    if created:
        update_transactions_category()


post_save.connect(category_keyword_post_save, sender=CategoryKeyword)


def category_keyword_post_delete(sender, instance, *args, **kwargs):
    """
    if a keyword is deleted,
    transactions with related category will have categoty set to none
    """
    modified_transactions = bank_account_statements.models.Transaction.objects.filter(
        category=instance.category
    )
    for transaction in modified_transactions:
        transaction.category = None
    bank_account_statements.models.Transaction.objects.bulk_update(
        modified_transactions, ["category"]
    )


post_delete.connect(category_keyword_post_delete, sender=CategoryKeyword)
