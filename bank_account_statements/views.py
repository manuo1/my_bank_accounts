from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, DeleteView

from bank_account_statements.forms import SatementForm
from .models import Statement


class StatementListView(ListView):
    model = Statement
    template_name = "statements_list.html"
    context_object_name = "statements"
    ordering = "date", "bank__name"


class StatementUploadView(CreateView):
    model = Statement
    form_class = SatementForm
    success_url = reverse_lazy("statements_list")
    template_name = "statement_upload.html"


class StatementDeleteView(DeleteView):
    model = Statement
    template_name = "statement_confirm_delete.html"
    success_url = reverse_lazy("statements_list")
