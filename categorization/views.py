from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from bank_account_statements.constants import STARTING_BANK_BALANCE
from bank_account_statements.models import Transaction
from categorization.constants import (
    SALARIES_CATEGORY_NAME,
    UNCATEGORIZABLE_TRANSACTION_CATEGORY_NAME,
)
from categorization.forms import (
    CategoryKeywordForm,
    CategoryForm,
    TransactionCustomLabelForm,
)
from categorization.models import Category, CategoryKeyword
from categorization.mutators import (
    toggle_between_none_and_uncategorisable as toggle_category,
)
from categorization.selectors import (
    get_balance,
    get_balance_after_fixed_costs,
    get_monthly_data,
)


class TransactionListView(ListView):
    model = Transaction
    template_name = "transactions_list.html"
    context_object_name = "transactions"
    paginate_by = 100
    uncategorizable = None

    def __init__(self, **kwargs):
        Category.objects.get_or_create(name=SALARIES_CATEGORY_NAME)
        self.uncategorizable = Category.objects.get_or_create(
            name=UNCATEGORIZABLE_TRANSACTION_CATEGORY_NAME
        )[0]
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uncategorizable"] = self.uncategorizable
        context["categories"] = Category.objects.all()
        context["category_value"] = self.kwargs.get("category_value")
        context["current_url"] = self.request.get_full_path
        return context

    def get_queryset(self):
        queryset = self.model.objects.none()
        search = self.request.GET.get("search")
        date_start = self.request.GET.get("date_start")
        date_end = self.request.GET.get("date_end")
        category_value = self.kwargs.get("category_value", "all")
        if category_value.isdigit():
            queryset = self.model.objects.filter(
                category__id=int(category_value)
            )
        if category_value == "all":
            queryset = self.model.objects.all()
        if category_value == "uncategorized":
            queryset = self.model.objects.filter(category__isnull=True)
        if search:
            queryset = queryset.filter(
                extended_label__icontains=search.replace(",", ".").replace(
                    "_", "/"
                )
            )
        if date_start:
            queryset = queryset.filter(date__gte=date_start)
        if date_end:
            queryset = queryset.filter(date__lt=date_end)

        return queryset

    def post(self, request, *args, **kwargs):
        transaction_id = request.POST.get("transaction_id")
        transaction = get_object_or_404(Transaction, pk=int(transaction_id))
        toggle_category(transaction)
        return self.get(request, *args, **kwargs)


class TransactionCustomLabelUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionCustomLabelForm
    success_url = reverse_lazy("transactions_list", args=["all"])
    template_name = "transaction_custom_label_update.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return "%s" % (next_url)
        return str(self.success_url)


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("transactions_list", args=["uncategorized"])
    template_name = "category_create.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return "%s" % (next_url)
        return str(self.success_url)


class CategoryKeywordCreateView(CreateView):
    model = CategoryKeyword
    form_class = CategoryKeywordForm
    success_url = reverse_lazy("transactions_list", args=["uncategorized"])
    template_name = "category_keyword_create.html"

    def get_initial(self):
        initial = super().get_initial()
        transaction = get_object_or_404(
            Transaction, id=self.kwargs.get("transaction_id")
        )
        initial["keyword"] = transaction.extended_label
        return initial

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url:
            return "%s" % (next_url)
        return str(self.success_url)


class DashboardListView(ListView):
    model = Transaction
    template_name = "dashboard.html"
    context_object_name = "transactions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["monthly_data"] = get_monthly_data()
        context["balance"] = get_balance()
        context["balance_after_fixed_costs"] = get_balance_after_fixed_costs()
        return context
