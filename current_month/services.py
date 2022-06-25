from decimal import Decimal, InvalidOperation
from current_month.constants import BANK_DATA_SPLITER
import dateparser
import json


def get_website_bank_transactions_in_bank_data(bank_data):
    json_object = json.loads(bank_data)
    return json_object["listeOperations"]


class WebSiteBankTransaction:
    pass


def string_value_to_decimal(string_value):
    value = None
    try:
        value = Decimal(string_value)
    except InvalidOperation:
        print(f"Impossible de convertir {string_value} en decimal")
    return value


def get_website_bank_transactions_in_raw_transactions(
    raw_website_bank_transactions,
):
    website_bank_transactions = []
    for raw_website_bank_transaction in raw_website_bank_transactions:
        website_bank_transaction = WebSiteBankTransaction()
        for key, value in raw_website_bank_transaction.items():
            setattr(website_bank_transaction, key, value)
        website_bank_transaction.dateOperation = dateparser.parse(
            website_bank_transaction.dateOperation
        )
        website_bank_transaction.dateValeur = dateparser.parse(
            website_bank_transaction.dateValeur
        )
        website_bank_transaction.montant = string_value_to_decimal(
            website_bank_transaction.montant
        )
        website_bank_transactions.append(website_bank_transaction)
    return website_bank_transactions


def get_transaction_label_in_website_bank_transaction(
    website_bank_transaction,
):
    label = (
        website_bank_transaction.libelleTypeOperation
        + " "
        + website_bank_transaction.libelleOperation
        + " "
        + website_bank_transaction.libelleComplementaire
        + " "
        + website_bank_transaction.referenceMandat
        + " "
        + website_bank_transaction.idCreancier
        + " "
        + website_bank_transaction.libelleCash1
        + " "
        + website_bank_transaction.libelleCash2
        + " "
        + website_bank_transaction.idCarte
        + " "
        + website_bank_transaction.referenceClient
    )
    while "  " in label:
        label = label.replace("  ", " ")
    return label
