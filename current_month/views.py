from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from categorization.models import Category
from current_month.constants import CREDIT_AGRICOLE_WEB_SITE_URL
from current_month.forms import BankWebSiteDataForm

from current_month.models import BankWebSiteData, TransactionWithoutStatement
from current_month.mutators import create_transactions_with_bank_web_site_data
from current_month.selectors import get_api_url


class TransactionWsListView(ListView):
    model = TransactionWithoutStatement
    template_name = "transactions_ws_list.html"
    context_object_name = "transactions"
    ordering = "date", "label"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # a suprimer par la suite
        create_transactions_with_bank_web_site_data()

        context["categories"] = Category.objects.all()
        context["current_url"] = self.request.get_full_path
        return context


class TransactionWSCreateView(CreateView):
    model = BankWebSiteData
    form_class = BankWebSiteDataForm
    success_url = reverse_lazy("transactions_ws_list")
    template_name = "raw_bank_data_input.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return "%s" % (next_url)
        return str(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ca_url"] = CREDIT_AGRICOLE_WEB_SITE_URL
        context["ca_api_url"] = get_api_url()
        return context
