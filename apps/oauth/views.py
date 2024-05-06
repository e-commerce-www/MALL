from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserEditForm
from django.core.paginator import Paginator
from django.db.models import Count

from apps.orders.models import Order
from apps.follows.models import Follows
from apps.songs.models import Song
from apps.sellers.models import Seller
from apps.payments.models import Payment


@login_required
def profile(request):
    
    if request.user.is_seller:
        profile_songs = Song.objects.filter(seller__user=request.user,)[:9]
    else:
        orders = Order.objects.filter(payment__is_paid=True, user=request.user).order_by('-created_at')[:9]
        profile_songs = [order.song for order in orders]
    
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)  # request.user는 현재 로그인한 사용자의 인스턴스
        if form.is_valid():
            form.save()
            return redirect('home')  # 프로필 페이지로 리다이렉트
        else:
            return render(request, 'accounts/profile.html', {'form': form, 'profile_songs': profile_songs})
    else:
        form = UserEditForm(instance=request.user)  # 폼을 초기화할 때 현재 사용자 정보로 채웁니다
    
    return render(request, 'accounts/profile.html', {'form': form, 'profile_songs': profile_songs})


@login_required
def purchase(request):
    orders = Order.objects.filter(payment__is_paid=True, user=request.user).order_by('-created_at')
    paginator = Paginator(orders, 10)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)

    return render(request, 'accounts/purchase_detail.html', context={"page_obj": page_obj, 'page_range': page_range})

@login_required
def sales(request):

    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        seller = None


    if seller:
        # 노래별로 주문 수 계산
        orders_by_song = Order.objects.filter(
            payment__is_paid=True,
            song__seller=seller
        ).values('song__title', 'song__created_at', 'song__price').annotate(order_count=Count('id'))
    else:
        orders_by_song = []


    # 페이지네이션
    paginator = Paginator(orders_by_song, 10)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)


    context={
        "page_obj": page_obj, 
        "page_range": page_range,
    }

    return render(request, 'accounts/sales_detail.html', context)



@login_required
def follower_recent(request):
    myfollow = Follows.objects.filter(follower=request.user)
    

    for se_follow in myfollow:
        # 각 팔로우한 유저 최근 음악 1개 가져오기
        seller_of_following = Seller.objects.get(user=se_follow.following)
        se_follow.recent_songs = Song.objects.filter(seller=seller_of_following).order_by('-id')[:1]

    paginator = Paginator(myfollow, 3)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)
    
    context={
        "page_obj": page_obj, 
        "page_range": page_range,
    }

    return render(request, 'accounts/following.html', context)



