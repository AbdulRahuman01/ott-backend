from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
import os
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from users.models import User
from django.http import HttpResponse


def create_admin(request):
    User = get_user_model()

    # Safety: do not create admin twice
    if User.objects.filter(is_superuser=True).exists():
        return JsonResponse(
            {"message": "Admin already exists"},
            status=400
        )

    # Create admin user
    User.objects.create_superuser(
        email=os.getenv("ADMIN_EMAIL", "admin@ottflix.com"),
        password=os.getenv("ADMIN_PASSWORD", "Admin@123"),
    )

    return JsonResponse({"message": "Admin created successfully"})

def go_to_admin_login(request):
    return redirect('/admin-panel/login/')


urlpatterns = [
    path('admin-panel/', include('admin_panel.urls')),
    path('', go_to_admin_login),
    path('admin/', admin.site.urls),

    path('movies/', include('movies.urls')),
    path('users/', include('users.urls')),
    path('reports/', include('reports.urls')),

    
   # 👈 THIS MUST BE INSIDE THE LIST
   path("create-admin/", create_admin),
]


# STATIC FILES (outside urlpatterns)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
