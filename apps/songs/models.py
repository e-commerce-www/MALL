from django.db import models
from taggit.managers import TaggableManager


# from django.contrib.auth import get_user_model

# User = get_user_model()
from apps.sellers.models import Seller

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=255)
    GENRE_CHOICES = (
        ('pop', '팝'),
        ('dance', '댄스'),
        ('edm', 'EDM'),
        ('hiphop', '힙합'),
        ('rnb', 'R&B'),
        ('classic', '클래식'),
        ('newage', '뉴에이지'),
        ('rock', '락'),
        ('ballad', '발라드'),
        ('indie', '인디'),
        ('jazz', '재즈/스윙'),
        ('latin', '라틴'),
        ('korea', '국악'),
        ('world', '월드뮤직'),
        ('ambient', '앰비언트'),
        ('trot', '트로트'),
        ('etc', '기타')
    )

    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='etc')
    tags = TaggableManager(blank=True)
    TEMPO_CHOICES = (
        ('slower', '아주 느림'),
        ('slow', '느림'),
        ('normal', '보통빠름'),
        ('fast', '빠름'),
        ('faster', '아주 빠름')
    )
    tempo = models.CharField(max_length=20, choices=TEMPO_CHOICES, default='normal')
    thumbnail = models.ImageField(upload_to='thumbnail/', blank=False)
    mp3 = models.FileField(upload_to='mp3/', blank=False)
    lyrics = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    