from django.urls import path
from .views import StatementListView, StatementUploadView, StatementDeleteView

urlpatterns = [
    path('statements/', StatementListView.as_view(), name='statements_list'),
    path('statements/upload/', StatementUploadView.as_view(), name='upload_statement'),
    path('statements/<pk>/delete/', StatementDeleteView.as_view(), name='delete_statement'),
]

