from django.urls import path

from . import views

app_name = 'oauth'
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('purchase/', views.purchase, name='purchase'),
    path('sales/', views.sales, name='sales'),
<<<<<<< HEAD
    path('download/', views.download, name='download'),
    path('follow/', views.follow, name='following'),
    path('unfollow/<int:pk>/', views.unfollow, name='unfollow'),
=======
    path('follow/', views.following, name='following'),
>>>>>>> f4a4d620f8c1229fbc43e5b7271c93b9b7580109
]