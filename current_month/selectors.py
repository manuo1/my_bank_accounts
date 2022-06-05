from datetime import datetime, timedelta
from bank_account_statements.constants import CREDIT_AGRICOLE
from current_month.constants import (
    API_BASE_URL as base,
    API_CONSTANT_PARAMS_START as const_start,
    API_PARAMS_START_DATE as start_date,
    API_PARAMS_END_DATE as end_date,
    API_CONSTANT_PARAMS_END as const_end,
    BANK_DATA_SPLITER,
)
import bank_account_statements
import current_month.models
from current_month.services import (
    get_raw_website_bank_transactions_in_bank_data,
    get_website_bank_transactions_in_raw_transactions,
)


def get_api_url():
    last_bank_statement_date = (
        bank_account_statements.models.Transaction.objects.filter(
            statement__bank__name=CREDIT_AGRICOLE
        )
        .order_by("date")
        .last()
        .date
    )
    last_bank_statement_datetime = datetime.combine(
        last_bank_statement_date, datetime.min.time()
    ) + timedelta(days=1)
    last_bank_statement_timestamp = (
        int(datetime.timestamp(last_bank_statement_datetime)) * 1000
    )
    now_timestamp = int(datetime.now().timestamp()) * 1000
    url = f"{base}{const_start}{start_date}{last_bank_statement_timestamp}{end_date}{now_timestamp}{const_end}"
    return url


def get_transactions_ws_list():
    bank_data = current_month.models.BankWebSiteData.objects.last().data
    raw_transactions_ws_list = get_raw_website_bank_transactions_in_bank_data(bank_data)
    website_bank_transactions = get_website_bank_transactions_in_raw_transactions(
        raw_transactions_ws_list
    )
    return website_bank_transactions
