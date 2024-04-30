from django.urls import path
from . import views

app_name = 'sellers'
urlpatterns = [
    path('apply/', views.seller_apply, name='seller_apply')
]