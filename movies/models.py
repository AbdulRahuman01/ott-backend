from django.db import models
from django.conf import settings
from cloudinary_storage.storage import RawMediaCloudinaryStorage

class Movie(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.IntegerField()
    duration = models.CharField(max_length=50)
    rating = models.CharField(max_length=20)
    poster = models.URLField()
    backdrop = models.URLField()   
    genre = models.CharField(max_length=200)        
    languages = models.CharField(max_length=200)        
    video_file = models.FileField(
    storage=RawMediaCloudinaryStorage(),
    null=True,
    blank=True
)
    # video_file = models.FileField(upload_to='videos/', null=True, blank=True)    
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_action = models.BooleanField(default=False)
    is_malayalam = models.BooleanField(default=False)
    is_scifi = models.BooleanField(default=False)
    is_comedy = models.BooleanField(default=False)   
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)       

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.IntegerField(default=1)   # 1⭐ to 5⭐
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")  # A user can review a movie ONLY once
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.email} → {self.movie.title} ({self.rating}⭐)"