from trace import Trace
from bank_account_statements.models import Transaction
from bank_account_statements.services import transaction_extended_label
from categorization.mutators import update_transactions_category
from current_month.selectors import get_transactions_without_statement_list
from current_month.services import (
    get_transaction_label_in_website_bank_transaction,
)


def create_transactions_with_bank_web_site_data():
    Transaction.objects.filter(statement__isnull=True).delete()
    website_bank_transactions = get_transactions_without_statement_list()
    transactions_instance_list = []
    for website_bank_transaction in website_bank_transactions:
        label = get_transaction_label_in_website_bank_transaction(
            website_bank_transaction
        )
        date = website_bank_transaction.dateOperation.date()
        value = website_bank_transaction.montant
        transaction = Transaction(
            date=date,
            label=label,
            value=value,
            extended_label=transaction_extended_label(
                label, "", value, date, ""
            ),
        )
        transactions_instance_list.append(transaction)
    Transaction.objects.bulk_create(transactions_instance_list)
    update_transactions_category()
