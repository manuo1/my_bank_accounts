from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from categorization.models import Category
from current_month.constants import CREDIT_AGRICOLE_WEB_SITE_URL
from current_month.forms import BankWebSiteDataForm

from current_month.models import BankWebSiteData
from current_month.selectors import get_api_url


class TransactionWSCreateView(CreateView):
    model = BankWebSiteData
    form_class = BankWebSiteDataForm
    success_url = reverse_lazy("transactions_list", args=["all"])
    template_name = "raw_bank_data_input.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return "%s" % (next_url)
        return str(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bank_website_url"] = CREDIT_AGRICOLE_WEB_SITE_URL
        context["bank_website_api_url"] = get_api_url()
        return context
