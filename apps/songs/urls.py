from django.urls import path
from . import views

app_name = "songs"

urlpatterns = [
    path("", views.song_list, name="chart"),
    path("chart/", views.song_list, name="song_list"),
    path("detail/<int:pk>/", views.song_detail, name="song_detail"),
]
