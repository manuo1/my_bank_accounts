from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView
from bank_account_statements.models import Transaction
from categorization.forms import CategoryKeywordForm, CategoryForm
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
        context["categories"] = Category.objects.order_by("name")
        context["filter"] = self.kwargs.get("filter")
        context["category_id"] = self.kwargs.get("category_id")
        return context

    def get_queryset(self):
        filter = self.kwargs.get("filter")
        category_id = self.kwargs.get("category_id")

        if filter == "all":
            return self.model.objects.order_by("-date", "label")
        if filter == "uncategorized":
            return self.model.objects.filter(category__isnull=True).order_by(
                "-date", "label"
            )
        if filter:
            return self.model.objects.filter(extended_label__icontains=filter).order_by(
                "-date", "label"
            )
        if category_id:
            return self.model.objects.filter(category__id=category_id).order_by(
                "-date", "label"
            )


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
        return initial
