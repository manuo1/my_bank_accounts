import os
from decouple import config
from django.core.wsgi import get_wsgi_application

setting_file = config("ENVIRONMENT")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"project.settings.{setting_file}")

application = get_wsgi_application()
