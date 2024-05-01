from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from .forms import UserEditForm
    

# Create your views here.
def profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)  # request.user는 현재 로그인한 사용자의 인스턴스
        if form.is_valid():
            form.save()
            return redirect('home')  # 프로필 페이지로 리다이렉트
        else:
            return render(request, 'accounts/profile.html', {'form': form})
    else:
        form = UserEditForm(instance=request.user)  # 폼을 초기화할 때 현재 사용자 정보로 채웁니다
    
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def purchase(request):
    orders = Order.objects.filter(user=request.user,payment__is_paid=True).order_by('-id')
    
    return render(request, 'accounts/purchase_detail.html', context={'orders': orders})

def sales(request):
    return render(request, 'accounts/sales_detail.html')

def download(request):
    orders = Order.objects.filter(user=request.user,payment__is_paid=True).order_by('-id')
    
    return render(request, 'accounts/download_detail.html', context={'orders': orders})

def following(request):
    return render(request, 'accounts/following.html')