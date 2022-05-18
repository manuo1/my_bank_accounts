from django.urls import path
from .views import StatementListView, StatementUploadView, StatementDeleteView

urlpatterns = [
    path("", StatementListView.as_view(), name="statements_list"),
    path("upload/", StatementUploadView.as_view(), name="upload_statement"),
    path(
        "<pk>/delete/",
        StatementDeleteView.as_view(),
        name="delete_statement",
    ),
]
