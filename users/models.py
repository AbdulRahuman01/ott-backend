from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,PermissionsMixin
from django.db import models 
from django.conf import settings
from movies.models import Movie
from datetime import timedelta
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



class Watchlist(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist_items')
     movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlisted_by')
     created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
         return f"{self.user.email} - {self.movie.title}"


class history(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='history_items')
     movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='viewed_by')
     watched_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
         return f"{self.user.email} watched {self.movie.title}"


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()  # fake price
    duration_days = models.IntegerField(default=30)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscription"
    )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} → {self.plan.name if self.plan else 'No Plan'}"

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.message}"
