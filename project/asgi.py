import os
from decouple import config
from django.core.asgi import get_asgi_application

setting_file = config('ENVIRONMENT')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"project.settings.{setting_file}")

application = get_asgi_application()
