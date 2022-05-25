import bank_account_statements.models
from bank_account_statements.services import unaccent
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
