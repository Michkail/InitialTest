"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.asgi import get_asgi_application
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.applications import Starlette
from starlette.routing import Mount
from pathlib import Path

# Path to collected static files
STATIC_ROOT = os.getenv('STATIC_ROOT', str(Path(__file__).resolve().parent.parent / "static"))

# Wrap Django ASGI app inside Starlette to serve static
django_asgi_app = get_asgi_application()

application = Starlette(
    routes=[
        Mount("/static", app=StaticFiles(directory=STATIC_ROOT), name="static"),
        Mount("/", app=django_asgi_app),
    ],
)
