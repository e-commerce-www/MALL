from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Follows(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together =  ('follower', 'following')
    
    def __str__(self):
        return f"{self.follower} follows {self.following}"
    