from django.shortcuts import get_object_or_404
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


class TransactionListView(ListView):
    model = Transaction
    template_name = "transactions_list.html"
    context_object_name = "transactions"
    paginate_by = 100
    search = None
    category_filter = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uncategorizable"] = Category.objects.get_or_create(
            name=UNCATEGORIZABLE_TRANSACTION_CATEGORY_NAME
        )[0]
        context["categories"] = Category.objects.all()
        context["filter"] = self.kwargs.get("filter")
        context["category_id"] = self.kwargs.get("category_id")
        context["current_url"] = self.request.path
        return context

    def get_queryset(self):
        filter = self.kwargs.get("filter")
        category_id = self.kwargs.get("category_id")

        if filter == "all":
            return self.model.objects.all()
        if filter == "uncategorized":
            return self.model.objects.filter(category__isnull=True)
        if filter:
            return self.model.objects.filter(extended_label__icontains=filter)
        if category_id:
            return self.model.objects.filter(category__id=category_id)


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
        initial["category"] = Category.objects.get(
            name=UNCATEGORIZABLE_TRANSACTION_CATEGORY_NAME
        )
        return initial


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "category_confirm_delete.html"
    success_url = reverse_lazy("transactions_list", args=["all"])
