from django.urls import path

from . import views

app_name = 'follows'
urlpatterns = [
    path('following/<int:pk>', views.follow_song, name='following'),
    # follow api
    path('follow/', views.follow, name='follow'),
    path('unfollow/', views.unfollow, name='unfollow'),
]