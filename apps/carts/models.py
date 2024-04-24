from django.db import models
from django.contrib.auth import get_user_model
from apps.songs.models import Song

User = get_user_model()

# Create your models here.
class Cart(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    