from django.urls import path
from . import views
urlpatterns = [
    # admin pages
    # API endpoints
    path('api/list/', views.movie_list, name='movie_list'),
    path('api/detail/<int:id>/', views.movie_detail, name='movie_detail'),
    path('api/reviews/add/', views.add_review, name='add_review'),
    path("api/reviews/<int:movie_id>/", views.get_movie_reviews),
    path("api/reviews/average/<int:movie_id>/", views.get_average_rating),
]
