from django.urls import path
from . import views

app_name ='carts'
urlpatterns = [
    path('', views.my_songs, name='my_songs'),
]