from unicodedata import category
from django.db.models import Sum, Value, DateField, Count

from bank_account_statements.models import Transaction
from categorization.constants import BASE_SALARY_VALUE, SALARIES_CATEGORY_NAME
from categorization.models import Category


def get_monthly_data():
    monthly_data = []
    first_salary_dates_of_the_month = []
    all_transactions = Transaction.objects.all()

    transaction_months = set([t.date.month for t in all_transactions])
    for month in transaction_months:
        # salary paiement at the end of the previous month
        salary_payment_transaction = (
            all_transactions.filter(
                category=Category.objects.get(name=SALARIES_CATEGORY_NAME),
                date__day__gte=20,
                value__gte=BASE_SALARY_VALUE,
                date__month=month,
            )
            .order_by("date")
            .first()
        )

        if salary_payment_transaction:
            first_salary_dates_of_the_month.append(salary_payment_transaction.date)
        else:
            # salary paiement at the start of the month
            salary_payment_transaction = (
                all_transactions.filter(
                    category=Category.objects.get(name=SALARIES_CATEGORY_NAME),
                    date__day__lte=5,
                    value__gte=BASE_SALARY_VALUE,
                    date__month=month + 1,
                )
                .order_by("date")
                .first()
            )
            if salary_payment_transaction:
                first_salary_dates_of_the_month.append(salary_payment_transaction.date)

    first_salary_dates_of_the_month.sort()
    for index, date in enumerate(first_salary_dates_of_the_month):
        if index < len(first_salary_dates_of_the_month) - 1:
            next_date = first_salary_dates_of_the_month[index + 1]

            months_in_transcations = list(
                Category.objects.filter(
                    transaction__date__gte=date,
                    transaction__date__lt=next_date,
                ).values_list("transaction__date__month", flat=True)
            )
            current_month = max(
                [
                    (months_in_transcations.count(value), value)
                    for value in months_in_transcations
                ]
            )[1]

            monthly_data.append(
                {
                    "displayed_date": date.replace(day=1, month=current_month),
                    "first_date": date,
                    "last_date": next_date,
                    "data": Category.objects.filter(
                        transaction__date__gte=date,
                        transaction__date__lt=next_date,
                    ).annotate(
                        sum_value=Sum("transaction__value"),
                        month=Value(date, DateField()),
                    ),
                }
            )

    return monthly_data
