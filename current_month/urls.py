from django.urls import path
from .views import TransactionWSCreateView

urlpatterns = [
    path(
        "transaction_ws/create",
        TransactionWSCreateView.as_view(),
        name="create_transaction_ws",
    ),
]
