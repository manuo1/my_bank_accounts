from django.db import models
from django.db.models.signals import post_save, post_delete
import bank_account_statements.models
from bank_account_statements.services import unaccent
from categorization.mutators import update_transactions_category


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)
    transactions_are_fixed_monthly_costs = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class CategoryKeyword(models.Model):

    keyword = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ["keyword"]

    def __str__(self) -> str:
        return f"{self.keyword} --> {self.category}"

    def save(self, *args, **kwargs):
        self.keyword = unaccent(self.keyword).lower()
        super().save(*args, **kwargs)
        update_transactions_category()


def category_keyword_post_delete(sender, instance, *args, **kwargs):
    """
    if a keyword is deleted,
    transactions with associated category will have their category set to none
    and apply the categorization again
    """
    modified_transactions = (
        bank_account_statements.models.Transaction.objects.filter(
            category=instance.category
        )
    )
    for transaction in modified_transactions:
        transaction.category = None
    bank_account_statements.models.Transaction.objects.bulk_update(
        modified_transactions, ["category"]
    )
    update_transactions_category()


post_delete.connect(category_keyword_post_delete, sender=CategoryKeyword)
