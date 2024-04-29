from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order

# Create your views here.
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def purchase(request):
    orders = Order.objects.filter(user=request.user,payment__is_paid=True).order_by('-id')
    
    return render(request, 'accounts/purchase_detail.html', context={'orders': orders})

def sales(request):
    return render(request, 'accounts/sales_detail.html')

def download(request):
    return render(request, 'accounts/download_detail.html')

def following(request):
    return render(request, 'accounts/following.html')