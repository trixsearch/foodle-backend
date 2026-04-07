"""
ASGI config for foodle_core.

Deploy with Uvicorn, for example:
    uvicorn foodle_core.asgi:application --host 0.0.0.0 --port 8000
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodle_core.settings')

application = get_asgi_application()
