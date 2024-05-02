from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserEditForm
from apps.orders.models import Order
from apps.follows.models import Follows
from apps.songs.models import Song
from apps.sellers.models import Seller


@login_required
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
    orders = Order.objects.filter(payment__is_paid=True, user=request.user)
    
    return render(request, 'accounts/purchase_detail.html', context={'orders': orders})

@login_required
def sales(request):
    return render(request, 'accounts/sales_detail.html')


@login_required
def follow(request):
    myfollow = Follows.objects.filter(follower=request.user)

    for se_follow in myfollow:
        # 각 팔로우한 유저 최근 음악 1개 가져오기
        seller_of_following = Seller.objects.get(user=se_follow.following)
        se_follow.recent_songs = Song.objects.filter(seller=seller_of_following).order_by('-id')[:1]

    return render(request, 'accounts/following.html', context = {'myfollow' : myfollow})


@login_required
def unfollow(request, pk):
    if request.method == 'POST':
        follow = get_object_or_404(Follows, pk=pk)
        follow.delete()

        return redirect('oauth:following')
    
    else:
        return HttpResponse("error")

