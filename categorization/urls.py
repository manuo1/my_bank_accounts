from django.urls import path

from categorization.views import (
    CategoryKeywordCreateView,
    CategoryCreateView,
    TransactionListView,
)

urlpatterns = [
    path(
        "<str:filter>",
        TransactionListView.as_view(),
        name="transactions_list",
    ),
    path(
        "category/<int:category_id>",
        TransactionListView.as_view(),
        name="categorized_transactions_list",
    ),
    path("category/create/", CategoryCreateView.as_view(), name="category_create"),
    path(
        "category_keyword/add_with_transaction_label/<int:transaction_id>",
        CategoryKeywordCreateView.as_view(),
        name="category_keyword_create",
    ),
]
