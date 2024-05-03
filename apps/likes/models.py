from django.db import models
from apps.songs.models import Song
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Like(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('song', 'user')