from django.shortcuts import render
from django.contrib.auth import authenticate
from ott_platform.decorators import login_required
import json
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from django.http import JsonResponse
from users.models import User, Watchlist, history, SubscriptionPlan, UserSubscription, Notification
from movies.models import Movie
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone



@api_view(['POST'])
@permission_classes((AllowAny,))

def Signup(request):
        email  = request.data.get("email")
        password = request.data.get("password")
        name = request.data.get("name")
        if not name or not email or not password:
            return Response({'message':'All fields are required'})
        if User.objects.filter(email=email).exists():
            return  JsonResponse({'message':'Email already exist'})
        user = User.objects.create_user(email=email,password=password)
        user.name = name
        user.save()
        return JsonResponse({'message':'user created successsfully'} ,status = 200)


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)

@api_view(["POST"])
@permission_classes([AllowAny])
def google_login(request):
    email = request.data.get("email")
    name = request.data.get("name")

    if not email:
        return JsonResponse({"error": "Email required"}, status=400)

    # Check if user exists
    user, created = User.objects.get_or_create(
        email=email,
        defaults={"name": name}
    )

    # Create token
    token, _ = Token.objects.get_or_create(user=user)

    return JsonResponse({"token": token.key})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_watchlist(request):

    user = request.user     # 🔥 user detected from token
    movie_id = request.data.get('movie_id')

    if not movie_id:
        return JsonResponse({'message': 'Movie ID is required'}, status=400)

    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie not found'}, status=404)

    # Check duplicate
    if Watchlist.objects.filter(user=user, movie=movie).exists():
        return JsonResponse({'message': 'Already in watchlist'}, status=200)

    Watchlist.objects.create(user=user, movie=movie)
    return JsonResponse({'message': 'Added to watchlist'}, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_watchlist(request):
    user = request.user  # 👈 TOKEN

    watchlist_items = Watchlist.objects.filter(user=user).select_related('movie')

    data = [
        {
            "movie_id": item.movie.id,
            "title": item.movie.title,
            "poster": item.movie.poster,
        }
        for item in watchlist_items
    ]

    return JsonResponse(data, safe=False, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_watchlist(request):
    user = request.user   # logged-in user from token

    movie_id = request.data.get('movie_id')

    if not movie_id:
        return Response({'message': 'Movie ID is required'}, status=400)

    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response({'message':'Movie not found'}, status=404)

    # Check if exists
    try:
        item = Watchlist.objects.get(user=user, movie=movie)
        item.delete()
        return Response({'message': 'Movie removed from watchlist'}, status=200)
    except Watchlist.DoesNotExist:
        return Response({'message': 'Movie not in watchlist'}, status=404)
     
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_history(request):
    movie_id = request.data.get("movie_id")

    if not movie_id:
        return JsonResponse({"message": "Movie ID required"}, status=400)

    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({"message": "Movie not found"}, status=404)

    entry, created = history.objects.get_or_create(
        user=request.user,
        movie=movie
    )

    return JsonResponse({"message": "History saved"}, status=200)


# -----------------------------
# GET HISTORY (NO USER_ID)
# -----------------------------
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_history(request):
    history_items = history.objects.filter(user=request.user).select_related("movie")

    data = [{
        "movie_id": item.movie.id,
        "title": item.movie.title,
        "poster": item.movie.poster,
        "watched_at": item.watched_at
    } for item in history_items]

    return JsonResponse(data, safe=False)


# -----------------------------
# CLEAR HISTORY
# -----------------------------
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def clear_history(request):
    history.objects.filter(user=request.user).delete()
    return JsonResponse({"message": "History cleared"}, status=200)


# -----------------------------
# REMOVE SPECIFIC MOVIE
# -----------------------------
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_history(request):
    movie_id = request.data.get("movie_id")

    if not movie_id:
        return JsonResponse({"message": "Movie ID required"}, status=400)

    history.objects.filter(user=request.user, movie_id=movie_id).delete()

    return JsonResponse({"message": "Removed from history"}, status=200)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        return JsonResponse({'message': 'Old password is incorrect'}, status=400)
    
    user.set_password(new_password)
    user.save()

    

    return JsonResponse({'message': 'Password changed successfully'}, status=200)


def get_plans(request):
    plans = SubscriptionPlan.objects.all()
    data = []
    for p in plans:
        data.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "duration": p.duration_days,
        })
    return JsonResponse(data, safe=False)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscribe(request):
    plan_id = request.data.get("plan_id")

    if not plan_id:
        return JsonResponse({"error": "Plan ID required"}, status=400)

    try:
        plan = SubscriptionPlan.objects.get(id=plan_id)
    except SubscriptionPlan.DoesNotExist:
        return JsonResponse({"error": "Plan not found"}, status=404)

    end_date = timezone.now() + timedelta(days=plan.duration_days)

    sub, created = UserSubscription.objects.update_or_create(
        user=request.user,
        defaults={
            "plan": plan,
            "start_date": timezone.now(),
            "end_date": end_date,
            "is_active": True,
        }
    )
    notify(request.user, f"You have successfully subscribed to the {plan.name} plan! Your subscription is active until {end_date.strftime('%Y-%m-%d')}.")

    return JsonResponse({
        "success": True,
        "message": f"Subscribed to {plan.name}",
        "plan": plan.name,
        "expires": end_date,
    })

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_subscription_status(request):

    try:
        sub = request.user.subscription
    except UserSubscription.DoesNotExist:
        return JsonResponse({"status": "none"})

    # Auto-expire
    if sub.end_date < timezone.now():
        sub.is_active = False
        sub.save()

    return JsonResponse({
        "status": "active" if sub.is_active else "expired",
        "plan": sub.plan.name,
        "expires": sub.end_date,
    })


def notify(user, msg):
    Notification.objects.create(user=user, message=msg)



@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by("-created_at")
    data = [
        {
            "id": n.id,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for n in notes
    ]
    return JsonResponse(data, safe=False)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({"message": "All notifications marked as read"})
