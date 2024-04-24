from django.db import models

from django.contrib.auth import get_user_model
from apps.songs.models import Song

User = get_user_model()

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, db_constraint=False)
    
    amount = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)