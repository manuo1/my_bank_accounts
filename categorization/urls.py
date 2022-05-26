from django.urls import path

from categorization.views import (
    CategoryDeleteView,
    CategoryKeywordCreateView,
    CategoryCreateView,
    TransactionCustomLabelUpdateView,
    TransactionListView,
)

urlpatterns = [
    path(
        "category/<str:category_value>",
        TransactionListView.as_view(),
        name="transactions_list",
    ),
    path(
        "<pk>/edit_custom_label",
        TransactionCustomLabelUpdateView.as_view(),
        name="edit_transaction_custom_label",
    ),
    path("category/create", CategoryCreateView.as_view(), name="category_create"),
    path(
        "category_keyword/add_with_transaction_label/<int:transaction_id>",
        CategoryKeywordCreateView.as_view(),
        name="category_keyword_create",
    ),
    path(
        "category/<pk>/delete",
        CategoryDeleteView.as_view(),
        name="delete_category",
    ),
]
