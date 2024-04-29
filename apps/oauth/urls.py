from django.urls import path

from . import views

app_name = 'oauth'
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('parchase/', views.purchase, name='purchase'),
    path('sales/', views.sales, name='sales'),
    path('download/', views.download, name='download'),
    path('follow/', views.following, name='following'),
]