from django.urls import path

from . import views

app_name = 'follows'
urlpatterns = [
    path('following/<int:pk>', views.follow_song, name='following'),
    path('add_follow/',views.add_follow, name ='add_follow'),
    
]