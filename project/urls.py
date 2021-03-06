from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from decouple import config
from categorization.views import DashboardListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("statements/", include("bank_account_statements.urls")),
    path("transactions/", include("categorization.urls")),
    path("dashboard/", DashboardListView.as_view(), name="dashboard"),
    path("current_month/", include("current_month.urls")),
]

# Add url to media files during development
if config("ENVIRONMENT") == "development":
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
