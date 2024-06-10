from django.urls import path
from . import views

app_name ='boards'
urlpatterns = [
    path('board_list/', views.board_list, name='board_list'),
    path('board_read/<int:pk>/', views.board_read, name='board_read'),
    path('board_create/', views.board_create, name='board_create'),
    path('comment_counts/', views.comment_count, name='comment_count'),
    path('board_update/<int:pk>/', views.board_update, name='board_update'),
    path('board_delete/<int:pk>/', views.board_delete, name='board_delete'),
    path('bookmarked/', views.bookmarked_boards, name='bookmarked_boards'),

]