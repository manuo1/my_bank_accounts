from decimal import Decimal, InvalidOperation
from current_month.constants import BANK_DATA_SPLITER
import dateparser
import json


def get_website_bank_transactions_in_bank_data(bank_data):
    json_object = json.loads(bank_data)
    return json_object["listeOperations"]


class WebSiteBankTransaction:
    pass


def get_website_bank_transactions_in_raw_transactions(
    raw_website_bank_transactions,
):
    website_bank_transactions = []
    for raw_website_bank_transaction in raw_website_bank_transactions:
        wbt = WebSiteBankTransaction()
        for key, value in raw_website_bank_transaction.items():
            setattr(wbt, key, value)
        wbt.dateOperation = dateparser.parse(wbt.dateOperation)
        wbt.dateValeur = dateparser.parse(wbt.dateValeur)
        wbt.montant = Decimal(wbt.montant)
        website_bank_transactions.append(wbt)
    return website_bank_transactions


def get_transaction_label_in_website_bank_transaction(
    website_bank_transaction,
):
    label = ""
    for attr in [
        "libelleOperation",
        "libelleTypeOperation",
        "libelleComplementaire",
        "referenceMandat",
        "idCreancier",
        "libelleCash1",
        "libelleCash2",
        "idCarte",
        "referenceClient",
    ]:

        label += getattr(website_bank_transaction, attr)

    while "  " in label:
        label = label.replace("  ", " ")
    return label
