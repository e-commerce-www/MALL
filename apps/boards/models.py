from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse

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

    def get_absolute_url(self):
        return reverse('boards:board_read', args=(self.pk, ))