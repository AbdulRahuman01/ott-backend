from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('signup/', views.Signup, name='signup'),
    path('login/', views.login, name='login'),
    path('google-login/', views.google_login, name='google_login'),
    path('watchlist/add/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', views.get_watchlist, name='get_watchlist'),
    path('watchlist/remove/', views.remove_from_watchlist, name='remove_from_watchlist'),   
    path('history/', views.get_history, name='get_viewing_history'),
    path('history/add/', views.add_history, name='add_to_viewing_history'),
    path('history/clear/', views.clear_history, name='clear_viewing_history'),
    path('history/remove/', views.remove_from_history, name='remove_from_viewing_history'),
    path('change-password/', views.change_password, name='change_password'),
    path("plans/", views.get_plans),
    path("subscribe/", views.subscribe),
    path("subscription/", views.get_subscription_status),
    path("notifications/", views.get_notifications),
    path("notifications/read/", views.mark_notifications_read),
    path('test/', lambda request: HttpResponse("USERS URL WORKING")),


]
