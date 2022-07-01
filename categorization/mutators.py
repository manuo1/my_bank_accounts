from unicodedata import category
import bank_account_statements.models
from bank_account_statements.services import unaccent
from categorization.constants import UNCATEGORIZABLE_TRANSACTION_CATEGORY_NAME
import categorization.models


def update_transactions_category():
    for category_keyword in categorization.models.CategoryKeyword.objects.all():
        bank_account_statements.models.Transaction.objects.filter(
            extended_label__icontains=category_keyword.keyword
        ).update(category=category_keyword.category)


def set_transaction_category(transaction, new_category):
    bank_account_statements.models.Transaction.objects.filter(id=transaction.id).update(
        category=new_category
    )


def toggle_between_none_and_uncategorisable(transaction):
    uncategorizable = categorization.models.Category.objects.get(
        name=UNCATEGORIZABLE_TRANSACTION_CATEGORY_NAME
    )
    if transaction.category is None:
        bank_account_statements.models.Transaction.objects.filter(
            id=transaction.id
        ).update(category=uncategorizable)

    if transaction.category == uncategorizable:
        bank_account_statements.models.Transaction.objects.filter(
            id=transaction.id
        ).update(category=None)
