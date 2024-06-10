from django.urls import path
from . import views

app_name = 'likes'
urlpatterns = [
    path('do/', views.like_do, name='like_do'),
    path('cancel/', views.like_cancel, name='like_cancel'),
    path('like_board/', views.board_like_do, name='like_board'),
    path('bookmark_do/', views.bookmark_do, name='bookmark_do'),

]