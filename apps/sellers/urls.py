from django.urls import path
from . import views

app_name = 'sellers'
urlpatterns = [
    path('apply/', views.seller_apply, name='seller_apply'),
    path('verify/', views.seller_verify, name='seller_verify'),
    path('upload/', views.seller_upload, name='seller_upload'),
    path('songs/', views.seller_songs, name='seller_songs'),
    path('<int:pk>/detail/', views.seller_detail, name='seller_detail'),
    path('<int:pk>/edit/', views.seller_edit, name='seller_edit'),
]