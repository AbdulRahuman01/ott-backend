from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

def go_to_admin_login(request):
    return redirect('/admin-panel/login/')

urlpatterns = [
    path('admin-panel/', include('admin_panel.urls')),
    path('',go_to_admin_login),   # 👈 ROOT → LOGIN
    path('admin/', admin.site.urls),
   
    path('movies/', include('movies.urls')),
    path('users/', include('users.urls')),
    path('reports/', include('reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
