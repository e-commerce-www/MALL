from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.
class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # 업데이트
        if self.pk: 
            self.updated_at = timezone.now()
        else:
            self.updated_at = None
        super(Board, self).save(*args, **kwargs)
    
    
class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.content
    
    def save(self, *args, **kwargs):
        # 업데이트
        if self.pk: 
            self.updated_at = timezone.now()
        else:
            self.updated_at = None
        super(Reply, self).save(*args, **kwargs)
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_likes')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'board'], name='unique_user_board_like')
        ]

    def __str__(self):
        return f'{self.user.username} like {self.board.title}'