from django.urls import path
from . import views


app_name = 'payments'
urlpatterns = [
    path('<int:pk>/pay/', views.payment_pay, name='payment_pay'),
    path('<int:pk>/verify/', views.payment_verify, name='payment_verify'),
    path('<int:pk>/detail/', views.payment_detail, name='payment_detail'),
]