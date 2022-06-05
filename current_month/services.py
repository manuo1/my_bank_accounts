from decimal import Decimal, InvalidOperation
from current_month.constants import BANK_DATA_SPLITER
import dateparser


def get_raw_website_bank_transactions_in_bank_data(bank_data):
    bank_data = bank_data.split(BANK_DATA_SPLITER)[1][2:-3]
    bank_data = bank_data.split("},{")
    return bank_data


def replace_char_in_string(my_string, index, char):
    return my_string[:index] + char + my_string[index + 1 :]


def identify_separators(raw_string):
    sought_string = ","
    index = 0
    # loop until all occurrences are found in text
    while True:
        # find() return the lowest index in the text where the sought_string is found
        index = raw_string.find(sought_string, index)
        # find () return -1 when sought_string is not found, all occurrences are found
        if index < 0:
            break
        # chars_around = [ 1 chars before the sought_string, 1 chars after the sought_string ]
        # fstring:1 will set the string to have a minimum of 1 chars
        chars_around = [
            f"{raw_string[index-1:index]:1}",
            f"{raw_string[index+len(sought_string):index+len(sought_string)+1]:1}",
        ]
        if chars_around == ['"', '"'] or (
            chars_around[1] == '"' and chars_around[0].isnumeric()
        ):
            raw_string = replace_char_in_string(raw_string, index, "#")

        # next index for next loop
        index += 1
    return raw_string


class WebSiteBankTransaction:
    pass


def string_value_to_decimal(string_value):
    value = None
    string_value = string_value.replace(",", ".").replace(" ", "")
    try:
        value = Decimal(string_value)
    except InvalidOperation:
        print(f"Impossible de convertir {string_value} en decimal")
    return value


def get_website_bank_transactions_in_raw_transactions(raw_website_bank_transactions):
    website_bank_transactions = []
    for raw_website_bank_transaction in raw_website_bank_transactions:
        raw_website_bank_transaction = (
            raw_website_bank_transaction.replace("\\u0026", "&")
            .replace("\\u0027", "'")
            .replace("\\u003d", "=")
        )
        raw_website_bank_transaction = identify_separators(raw_website_bank_transaction)
        transaction_data = raw_website_bank_transaction.split("#")
        website_bank_transaction = WebSiteBankTransaction()
        for raw_field_value in transaction_data:
            raw_field_value = (
                raw_field_value.replace('":', '"#').replace('"', "").split("#")
            )
            setattr(website_bank_transaction, raw_field_value[0], raw_field_value[1])
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
