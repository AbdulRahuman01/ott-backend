from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

from users.models import User
from django.http import HttpResponse


def reset_admin(request):
    admin = User.objects.filter(email="admin@gmail.com").first()

    if not admin:
        admin = User.objects.create(
            email="admin@gmail.com",
            is_admin=True
        )

    admin.set_password("admin123")
    admin.save()

    return HttpResponse("Admin created/reset successfully")



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
]


# STATIC FILES (outside urlpatterns)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
