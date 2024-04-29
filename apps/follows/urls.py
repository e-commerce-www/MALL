from django.urls import path
from . import views

app_name = 'follows'
urlpatterns = [
    # 다른 URL 패턴들...
    path('unfollow/<int:follow_id>/', views.unfollow, name='unfollow'),
]