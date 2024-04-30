from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.db.models import Max
from apps.orders.models import Order
from apps.follows.models import Follows


# Create your views here.
@login_required
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



@login_required
def unfollow(request, pk):
    if request.method == 'POST':
        follow = get_object_or_404(Follows, pk=pk)
        follow.delete()

        return redirect('oauth:following')
    
    else:
        return HttpResponseNotAllowed(['POST'])
    

# @login_required
# def recent_activity(request):
#     following_users = request.user.following_set.all()

#     # 각 사용자별로 올린 최근 노래
#     recent_songs = []
#     for user in following_users:
#         latest_song_date = user.song_set.aggregate(latest_date = Max('created_at'))['latest_date']
#         recent_song = user.song_set.filter(created_at = latest_song_date).first()

#         if recent_songs:
#             recent_songs.append(recent_song)

#     return render(request, 'accounts/following.html', context = {'recent_song' : recent_song})