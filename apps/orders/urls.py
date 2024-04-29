from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.order_list, name='history'),
    path('history/', views.order_list, name='order_list'),
    path('<int:pk>/detail/', views.order_detail, name='order_detail'),
    
]