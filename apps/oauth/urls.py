from django.urls import path

from . import views

app_name = 'oauth'
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('purchase/', views.purchase, name='purchase'),
    path('sales/', views.sales, name='sales'),
    path('follow/', views.follower_recent, name='following'),
]