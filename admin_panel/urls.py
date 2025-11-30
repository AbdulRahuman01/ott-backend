from django.urls import path
from . import views

urlpatterns = [
    # AUTH
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    # DASHBOARD
    path('dashboard/', views.dashboard, name='admin_dashboard'),

    # MOVIE MANAGEMENT
    path('movies/', views.movies_list, name='admin_movies'),
    path('movies/add/', views.add_movie, name='admin_add_movie'),
    path('movies/edit/<int:id>/', views.edit_movie, name='admin_edit_movie'),
    path('movies/delete/<int:id>/', views.delete_movie, name='admin_delete_movie'),

    # User Management
    path('users/', views.users_list, name='admin_users'),
    path('users/block/<int:id>/', views.block_user, name='block_user'),
    path('users/unblock/<int:id>/', views.unblock_user, name='unblock_user'),
    path('users/activity/<int:id>/', views.user_activity, name='user_activity'),

    # REPORTS
    path("reports/", views.reports_dashboard, name="reports_dashboard"),
]
