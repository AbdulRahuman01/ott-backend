"""
WSGI config for ott_platform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ott_platform.settings')

application = get_wsgi_application()

from django.contrib.auth import get_user_model

if os.environ.get("RENDER") == "true":
    User = get_user_model()
    admin_email = "admin@gmail.com"
    admin_password = "Admin@123"

    if not User.objects.filter(email=admin_email).exists():
        User.objects.create_superuser(
            email=admin_email,
            password=admin_password,
            name="Admin"
        )