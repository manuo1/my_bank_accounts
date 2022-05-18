from django.urls import path

from categorization.views import TransactionListView

urlpatterns = [
    path("", TransactionListView.as_view(), name="transactions_list"),
]
