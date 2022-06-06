from django.db.models import Sum, Value, DateField
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from bank_account_statements.models import Transaction
from categorization.constants import BASE_SALARY_VALUE, SALARIES_CATEGORY_NAME
from categorization.models import Category
from categorization.constants import (
    QUANTITY_OF_MONTHS_DISPLAYED_IN_THE_DASHBOARD as month_qty,
)


def get_monthly_data():
    monthly_data = []
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
    for index, start_date in enumerate(first_salary_dates_of_the_month):
        if index < len(first_salary_dates_of_the_month) - 1:
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
