from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from users.models import User   # your custom user
from movies.models import Movie
from users.models import Watchlist, history 
from django.db.models import Count
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from users.models import SubscriptionPlan
from django.contrib import messages

def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password!")
            return render(request, "admin_panel/login.html")

        if not user.is_admin:
            messages.error(request, "You are not an admin!")
            return render(request, "admin_panel/login.html")

        # Successful login
        login(request, user)
        return redirect("admin_dashboard")

    return render(request, "admin_panel/login.html")

def admin_logout(request):
    logout(request)
    return redirect("admin_login")

def dashboard(request):

    # only admin allowed
    if not request.user.is_authenticated or not request.user.is_admin:
        return redirect('admin_login')

    total_movies = Movie.objects.count()
    total_users = User.objects.count()
    total_watchlist = Watchlist.objects.count()
    total_history = history.objects.count()

    context = {
        "total_movies": total_movies,
        "total_users": total_users,
        "total_watchlist": total_watchlist,
        "total_history": total_history,
    }

    return render(request, 'admin_panel/dashboard.html', context)

from movies.models import Movie
from django.contrib import messages

def movies_list(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        return redirect('admin_login')

    movies = Movie.objects.all().order_by('-id')
    paginator = Paginator(movies, 5)  # 8 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "admin_panel/movies_list.html", {
        "movies": page_obj,   # send page_obj instead of movies
        "page_obj": page_obj
    })



def add_movie(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        return redirect('admin_login')

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        year = request.POST.get("year")
        duration = request.POST.get("duration")
        rating = request.POST.get("rating")
        poster = request.POST.get("poster")
        backdrop = request.POST.get("backdrop")
        genre = request.POST.get("genre")
        languages = request.POST.get("languages")

        video_file = request.FILES.get("video_file")

        is_featured = request.POST.get("is_featured") == "on"
        is_trending = request.POST.get("is_trending") == "on"
        is_action = request.POST.get("is_action") == "on"
        is_malayalam = request.POST.get("is_malayalam") == "on"
        is_scifi = request.POST.get("is_scifi") == "on"
        is_comedy = request.POST.get("is_comedy") == "on"
        is_premium = request.POST.get("is_premium") == "on"

        Movie.objects.create(
            title=title,
            description=description,
            year=year,
            duration=duration,
            rating=rating,
            poster=poster,
            backdrop=backdrop,
            genre=genre,
            languages=languages,
            video_file=video_file,
            is_featured=is_featured,
            is_trending=is_trending,
            is_action=is_action,
            is_malayalam=is_malayalam,
            is_scifi=is_scifi,
            is_comedy=is_comedy,
            is_premium=is_premium,
        )

        messages.success(request, "Movie added successfully!")
        return redirect("admin_movies")

    return render(request, "admin_panel/add_movie.html")

from movies.models import Movie
from django.contrib import messages

def edit_movie(request, id):
    if not request.user.is_authenticated or not request.user.is_admin:
        return redirect("admin_login")

    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return redirect("admin_movies")

    if request.method == "POST":
        movie.title = request.POST.get("title")
        movie.description = request.POST.get("description")
        movie.year = request.POST.get("year")
        movie.duration = request.POST.get("duration")
        movie.rating = request.POST.get("rating")
        movie.poster = request.POST.get("poster")
        movie.backdrop = request.POST.get("backdrop")
        movie.genre = request.POST.get("genre")
        movie.languages = request.POST.get("languages")

        if request.FILES.get("video_file"):
            movie.video_file = request.FILES.get("video_file")

        movie.is_featured = request.POST.get("is_featured") == "on"
        movie.is_trending = request.POST.get("is_trending") == "on"
        movie.is_action = request.POST.get("is_action") == "on"
        movie.is_malayalam = request.POST.get("is_malayalam") == "on"
        movie.is_scifi = request.POST.get("is_scifi") == "on"
        movie.is_comedy = request.POST.get("is_comedy") == "on"
        movie.is_premium = request.POST.get("is_premium") == "on"

        movie.save()

        messages.success(request, "Movie updated successfully!")
        return redirect("admin_movies")

    return render(request, "admin_panel/edit_movie.html", {"movie": movie})

from movies.models import Movie
from django.contrib import messages

def delete_movie(request, id):
    if not request.user.is_authenticated or not request.user.is_admin:
        return redirect("admin_login")

    try:
        movie = Movie.objects.get(id=id)
        movie.delete()
        messages.success(request, "Movie deleted successfully!")
    except Movie.DoesNotExist:
        messages.error(request, "Movie not found!")

    return redirect("admin_movies")


def users_list(request):
    users = User.objects.all().order_by('id')
    return render(request, 'admin_panel/users_list.html', {"users": users})

def block_user(request, id):
    user = get_object_or_404(User, id=id)
    user.is_active = False
    user.save()
    return redirect('admin_users')

def unblock_user(request, id):
    user = get_object_or_404(User, id=id)
    user.is_active = True
    user.save()
    return redirect('admin_users')

def user_activity(request, id):
    user = get_object_or_404(User, id=id)

    watchlist_items = Watchlist.objects.filter(user=user)
    history_items = history.objects.filter(user=user)

    context = {
        "user": user,
        "watchlist": watchlist_items,
        "history": history_items
    }
    return render(request, 'admin_panel/user_activity.html', context)

# Report Views
def reports_dashboard(request):
    # 1️⃣ Most Watched Movies
    top_movies = Movie.objects.annotate(
        watch_count=Count("viewed_by")  # related_name in history model
    ).order_by("-watch_count")[:10]

    # 2️⃣ Most Active Users
    top_users = User.objects.annotate(
        watch_count=Count("history_items")  # related_name in history model
    ).order_by("-watch_count")[:10]

    # 3️⃣ Most Watchlisted Movies (optional)
    most_watchlisted = Movie.objects.annotate(
        watchlist_count=Count("watchlisted_by")  # related_name in Watchlist
    ).order_by("-watchlist_count")[:10]

    context = {
        "top_movies": top_movies,
        "top_users": top_users,
        "most_watchlisted": most_watchlisted,
    }

    return render(request, "admin_panel/reports.html", context)

@login_required
def plan_list(request):
    plans=SubscriptionPlan.objects.all()
    return render(request,"admin_panel/plan_list.html",{"plans":plans})

@login_required
def add_plan(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        duration = request.POST.get("duration")

        SubscriptionPlan.objects.create(
            name=name,
            price=price,
            duration_days=duration
        )

        messages.success(request, "Plan added successfully!")
        return redirect("admin_plans")

    return render(request, "admin_panel/add_plan.html")

@login_required
def edit_plan(request, id):
    plan = SubscriptionPlan.objects.get(id=id)

    if request.method == "POST":
        plan.name = request.POST.get("name")
        plan.price = request.POST.get("price")
        plan.duration_days = request.POST.get("duration")
        plan.save()

        messages.success(request, "Plan updated successfully!")
        return redirect("admin_plans")

    return render(request, "admin_panel/edit_plan.html", {"plan": plan})

@login_required
def delete_plan(request, id):
    plan = SubscriptionPlan.objects.get(id=id)
    plan.delete()
    messages.success(request, "Plan deleted successfully!")
    return redirect("admin_plans")
