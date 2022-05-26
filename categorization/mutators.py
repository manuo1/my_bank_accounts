import bank_account_statements.models
from bank_account_statements.services import unaccent
from categorization.constants import UNCATEGORIZABLE_TRANSACTION_CATEGORY_NAME
import categorization.models


def update_transactions_category():
    transactions = bank_account_statements.models.Transaction.objects.all()
    category_keywords = categorization.models.CategoryKeyword.objects.all()
    for transaction in transactions:
        for category_keyword in category_keywords:
            if category_keyword.keyword in unaccent(transaction.extended_label).lower():
                if transaction.category != category_keyword.category:
                    transaction.category = category_keyword.category

    bank_account_statements.models.Transaction.objects.bulk_update(
        transactions, ["category"]
    )


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

    # desactivated, bugged function set to uncategorizable the wrong transaction
    # if transaction.category == uncategorizable:
    #     bank_account_statements.models.Transaction.objects.filter(
    #         id=transaction.id
    #     ).update(category=None)
