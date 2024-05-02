"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from . import views

handler404 = 'config.views.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('songs/', include('apps.songs.urls')),
    path('accounts/', RedirectView.as_view(url='/home'), name='home_redirect'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('apps.oauth.urls')),
    path('sellers/', include('apps.sellers.urls')),
    path('orders/', include('apps.orders.urls')),
    path('mySongs/', include('apps.carts.urls')),
    path('search/', views.SearchFormView.as_view(), name='search'),
    path('payments/', include('apps.payments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

