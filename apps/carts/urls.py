from django.urls import path
from . import views

app_name ='carts'
urlpatterns = [
    path('', views.my_songs, name='my_songs'),
    path('add/', views.add_song, name='add_song'),
    path('remove/', views.remove_song, name='remove_song'),
]