from datetime import datetime
from decimal import Decimal
from unicodedata import category
from django.db.models import Sum, Value, DateField
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from bank_account_statements.constants import STARTING_BANK_BALANCE
from bank_account_statements.models import Transaction
from categorization.constants import (
    BASE_SALARY_VALUE,
    NUMBER_OF_MONTHS_TO_CALCULATE_AVERAGE_FIXED_COSTS as FIXED_COST_MONTHS_QTY,
    SALARIES_CATEGORY_NAME,
)
from categorization.models import Category
from categorization.constants import (
    QUANTITY_OF_MONTHS_DISPLAYED_IN_THE_DASHBOARD as MONTH_QTY,
)


def get_first_salary_dates_of_the_month(month_qty):
    first_salary_dates_of_the_month = []
    all_transactions = Transaction.objects.all().order_by("date")
    last_month = all_transactions.last().date.replace(day=1)
    month_list = []
    for qty in range(month_qty):
        month_list.append(last_month - relativedelta(months=qty))
    for start_date in month_list:
        salary_payment_transaction = (
            all_transactions.filter(
                category=Category.objects.get(name=SALARIES_CATEGORY_NAME),
                value__gte=BASE_SALARY_VALUE,
                date__gte=start_date.replace(day=20),
            )
            .order_by("date")
            .first()
        )
        if salary_payment_transaction:
            first_salary_dates_of_the_month.append(salary_payment_transaction.date)

    first_salary_dates_of_the_month.append((timezone.now() + timedelta(days=1)).date())
    first_salary_dates_of_the_month.sort()
    return first_salary_dates_of_the_month


def get_monthly_data():
    monthly_data = []
    first_salary_dates_of_the_month = get_first_salary_dates_of_the_month(MONTH_QTY)
    for index, start_date in enumerate(first_salary_dates_of_the_month[:-1]):
        end_date = first_salary_dates_of_the_month[index + 1]

        data = Category.objects.filter(
            transaction__date__gte=start_date,
            transaction__date__lt=end_date,
        ).annotate(
            sum_value=Sum("transaction__value"),
            month=Value(start_date, DateField()),
        )
        monthly_data.append(
            {
                "displayed_date": end_date.replace(day=1),
                "first_date": start_date,
                "last_date": end_date,
                "data": data,
                "total_value": sum([c.sum_value for c in data]),
            }
        )
    return monthly_data


def get_balance_after_fixed_costs():
    balance_after_fixed_costs = {
        "monthly": 0,
        "weekly": 0,
        "daily": 0,
    }
    salary_date_list = get_first_salary_dates_of_the_month(FIXED_COST_MONTHS_QTY + 2)
    month_fixed_costs = []
    for index, first_salary_date in enumerate(salary_date_list[:-1]):
        month_fixed_costs.append(
            Category.objects.filter(
                transaction__date__gte=first_salary_date,
                transaction__date__lt=salary_date_list[index + 1],
                transactions_are_fixed_monthly_costs=True,
            ).aggregate(Sum("transaction__value"))["transaction__value__sum"]
            * -1
        )
    max_monthly_fixed_cost = max(month_fixed_costs)

    current_month_expenses_excluding_fixed_costs = Category.objects.filter(
        transaction__date__gte=salary_date_list[-2],
        transactions_are_fixed_monthly_costs=False,
    ).aggregate(Sum("transaction__value"))["transaction__value__sum"]

    balance_after_fixed_costs = {
        "monthly": current_month_expenses_excluding_fixed_costs - max_monthly_fixed_cost
    }
    estimated_date_of_next_salary = salary_date_list[-2] + relativedelta(months=1)
    days_until_next_salary = (
        estimated_date_of_next_salary - datetime.now().date()
    ).days
    if balance_after_fixed_costs["monthly"] >= 0:
        balance_after_fixed_costs["daily"] = (
            balance_after_fixed_costs["monthly"] / days_until_next_salary
        )
        balance_after_fixed_costs["weekly"] = (
            balance_after_fixed_costs["monthly"] / days_until_next_salary
        ) * 7

    return balance_after_fixed_costs


def get_balance():
    return {
        "value": Transaction.objects.all().aggregate(Sum("value"))["value__sum"]
        + Decimal(STARTING_BANK_BALANCE),
        "date": Transaction.objects.order_by("date").last().date,
    }
