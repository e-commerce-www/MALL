from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from apps.follows.models import Follows


# Create your views here.
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def purchase(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    
    return render(request, 'accounts/purchase_detail.html', context={'orders': orders})

def sales(request):
    return render(request, 'accounts/sales_detail.html')

def download(request):
    return render(request, 'accounts/download_detail.html')

@login_required
def following(request):
    follows = Follows.objects.filter(follower=request.user)
    return render(request, 'accounts/following.html', context= {'follows':follows})