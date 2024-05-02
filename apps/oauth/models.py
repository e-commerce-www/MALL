from django.db import models

from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    profile = models.ImageField(upload_to='profiles/', default='profiles/default.png', blank=False)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.username