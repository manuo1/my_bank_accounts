from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from bank_account_statements.models import Transaction
from categorization.constants import UNCATEGORIZABLE_TRANSACTION_CATEGORY_NAME
from categorization.forms import (
    CategoryKeywordForm,
    CategoryForm,
    TransactionCustomLabelForm,
)
from categorization.models import Category, CategoryKeyword
from categorization.mutators import (
    toggle_between_none_and_uncategorisable as toggle_category,
)


class TransactionListView(ListView):
    model = Transaction
    template_name = "transactions_list.html"
    context_object_name = "transactions"
    paginate_by = 100
    uncategorizable = None

    def __init__(self, **kwargs):
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
        category_value = self.kwargs.get("category_value", "all")
        if category_value.isdigit():
            queryset = self.model.objects.filter(category__id=int(category_value))
        if category_value == "all":
            queryset = self.model.objects.all()
        if category_value == "uncategorized":
            queryset = self.model.objects.filter(category__isnull=True)
        if search:
            queryset = queryset.filter(
                extended_label__icontains=search.replace(",", ".").replace("_", "/")
            )
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
