from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.db import models 
from django.conf import settings
from movies.models import Movie

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
        User.is_superuser = True 
        user.save(using=self._db) 
        return user 
 
class User(AbstractBaseUser): 
    email = models.EmailField(unique=True) 
    name = models.CharField(max_length =255) 
    is_active = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False) 
    objects = UserManager() 
 
    USERNAME_FIELD = 'email'


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

