from django.urls import path
from . import views

app_name = "songs"

urlpatterns = [
    path("", views.song_list, name="chart"),
    path("chart/", views.song_list, name="song_list"),
    path("<int:pk>/detail/", views.song_detail, name="song_detail"),
    path('lyrics/', views.song_lyrics, name='song_lyrics'),
    path('recent/', views.song_recent, name='song_recent'),
    path('ranking/', views.song_ranking, name='song_ranking'),
    path('genre/', views.song_genre, name='song_genre'),
    path('tempo/', views.song_tempo, name='song_tempo'),
    
]
