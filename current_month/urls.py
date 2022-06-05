from django.urls import path
from .views import TransactionWsListView, TransactionWSCreateView

urlpatterns = [
    path(
        "transactions_ws",
        TransactionWsListView.as_view(),
        name="transactions_ws_list",
    ),
    path(
        "transaction_ws/create",
        TransactionWSCreateView.as_view(),
        name="create_transaction_ws",
    ),
]
