from django.views.generic import ListView
from bank_account_statements.models import Transaction


class TransactionListView(ListView):
    model = Transaction
    template_name = "transactions_list.html"
    context_object_name = "transactions"
    ordering = "date", "label"
    paginate_by = 100
