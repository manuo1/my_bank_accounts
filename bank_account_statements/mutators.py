from bank_account_statements.constants import CREDIT_AGRICOLE, CREDIT_MUTUEL
import bank_account_statements.models
from bank_account_statements.services import (
    CreditAgricolPdfStatement,
    CreditMutuelPdfStatement,
    common_date_format,
    transaction_extended_label,
)


def create_transaction_with_statement(instance):
    transactions_instance_list = []

    if instance.bank.name == CREDIT_MUTUEL:
        pdf_statement = CreditMutuelPdfStatement()

    if instance.bank.name == CREDIT_AGRICOLE:
        pdf_statement = CreditAgricolPdfStatement()

    for transaction in pdf_statement.get_transactions(instance.file.path):
        transactions_instance_list.append(
            bank_account_statements.models.Transaction(
                statement=instance,
                date=transaction[0],
                label=transaction[1],
                value=transaction[2],
                extended_label=transaction_extended_label(
                    label=transaction[1],
                    custom_label="",
                    value=transaction[2],
                    date=transaction[0],
                    statement_bank_name=instance.bank.name,
                ),
            )
        )
    bank_account_statements.models.Transaction.objects.bulk_create(
        transactions_instance_list
    )
