from django.urls import path
from .views import BankListView, StatementListView, StatementUploadView, StatementDeleteView

urlpatterns = [
    path('banks/', BankListView.as_view(),name='banks'),
    path('statements/', StatementListView.as_view(), name='statements_list'),
    path('statements/upload/', StatementUploadView.as_view(), name='upload_statement'),
    path('statements/<pk>/delete/', StatementDeleteView.as_view(), name='delete_statement'),
]

