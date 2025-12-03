from django.shortcuts import render,redirect
from ott_platform.decorators import login_required
from django.http import JsonResponse,HttpResponse
from .models import Movie, Review
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



def movie_list(request):
    movies = Movie.objects.all()

    movie_data = []
    for mv in movies:
        movie_data.append({
            "id": mv.id,
            "title": mv.title,
            "description": mv.description,
            "year": mv.year,
            "duration": mv.duration,
            "rating": mv.rating,
            "poster": mv.poster,
            "backdrop": mv.backdrop,
            "genre": mv.genre,
            "languages": mv.languages,
            "video_url": request.build_absolute_uri(mv.video_file.url) if mv.video_file else None,
            "is_featured": mv.is_featured,
            "is_trending": mv.is_trending,
            "is_action": mv.is_action,
            "is_comedy": mv.is_comedy,
            "is_malayalam": mv.is_malayalam,
            "is_scifi": mv.is_scifi,
            "is_premium": mv.is_premium,
        })

    return JsonResponse(movie_data, safe=False)


def movie_detail(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return JsonResponse({"message": "Movie not found"}, status=404)

    data = {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "year": movie.year,
        "duration": movie.duration,
        "rating": movie.rating,
        "poster": movie.poster,
        "backdrop": movie.backdrop,
        "genre": movie.genre,
        "languages": movie.languages,
        # MAIN PART: Return video file full URL
        "video_url": request.build_absolute_uri(movie.video_file.url) if movie.video_file else None,
        "is_premium": movie.is_premium,
    }

    return JsonResponse(data, status=200)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_review(request):

    movie_id = request.data.get("movie_id")
    rating = request.data.get("rating")
    comment = request.data.get("comment", "")

    if not movie_id or not rating:
        return JsonResponse({"error": "movie_id and rating required"}, status=400)

    # Load movie
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({"error": "Movie not found"}, status=404)

    # Create or update review
    review, created = Review.objects.update_or_create(
        user=request.user,
        movie=movie,
        defaults={"rating": rating, "comment": comment}
    )

    return JsonResponse({
        "success": True,
        "message": "Review added" if created else "Review updated"
    })


def get_movie_reviews(request, movie_id):
    reviews = Review.objects.filter(movie_id=movie_id).select_related("user")

    data = [
        {
            "user": r.user.email,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at.strftime("%Y-%m-%d")
        }
        for r in reviews
    ]

    return JsonResponse(data, safe=False)

from django.db.models import Avg

def get_average_rating(request, movie_id):
    avg = Review.objects.filter(movie_id=movie_id).aggregate(avg=Avg("rating"))["avg"]

    return JsonResponse({
        "average": round(avg or 0, 1)
    })
