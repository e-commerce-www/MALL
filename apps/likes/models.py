from django.db import models
from apps.songs.models import Song
from apps.boards.models import Board
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Like(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('song', 'user')
        
    def __str__(self):
        return self.song.title
 
    
class BoardLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_likes')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'board'], name='unique_user_board_like')
        ]

    def __str__(self):
        return f'{self.user.username} like {self.board.title}'


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bookmarks')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_bookmarks')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'board'], name='unique_user_board_bookmark')
        ]

    def __str__(self):
        return f'{self.user.username} bookmarked {self.board.title}'