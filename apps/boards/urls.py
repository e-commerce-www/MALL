from django.urls import path
from . import views

app_name ='boards'
urlpatterns = [
    path('board_list/', views.board_list, name='board_list'),
    path('board_read/<int:pk>/', views.board_read, name='board_read'),
    path('board_create/', views.board_create, name='board_create'),
    path('comment_create/<int:pk>', views.comment_create, name='comment_create'),


]