from django.shortcuts import render
from django.urls import reverse
from apps.songs.models import Song
from apps.orders.models import Order
from django.http import JsonResponse
from config.forms import SearchForm
from apps.songs.services import ranked_songs
from apps.carts.models import Cart
import json
from django.contrib.auth.decorators import login_required
import random


# def song_recommend(user):
#     # 유저의 찜한목록을 가져온다
#     user_cart_songs = Cart.objects.filter(user=user)
    
#     # 유저의 찜한 목록에서 음악의 ID를 가져온다
#     user_song_ids = user_cart_songs.values_list('song_id', flat=True)
    
#     # 카트에 담긴 음악의 장르들을 가져오고, 그 장르의 음악들을 뽑은 후, 유저의 찜한 음악 목록에 이미 있는 곡들은 제외한 후, 랜덤으로 4개의 곡을 표시함
#     # 추가 하고싶은 로직은 여기에 넣으면 됩니다.
#     recommended_songs = Song.objects.filter(genre__in=Song.objects.filter(id__in=user_song_ids).values_list('genre', flat=True)).exclude(id__in=user_song_ids).order_by('?')[:4]
    
#     return recommended_songs


# def home(request):
#     songs = Song.objects.all().order_by('-created_at')[:5] # 노래 가져오기 예시
#     ranking_songs = ranked_songs()[:5]
#     recommended_songs = song_recommend(request.user) if request.user.is_authenticated else None



from django.shortcuts import render
from apps.songs.models import Song
from apps.orders.models import Order
from django.http import JsonResponse
from config.forms import SearchForm
from apps.songs.services import ranked_songs
import json
import random

from django.shortcuts import render
from apps.songs.models import Song
from apps.orders.models import Order
from apps.songs.services import ranked_songs
import random

def get_random_ranking_songs(count=4):
    """상위 20개의 랭킹 노래 중에서 주어진 개수만큼 랜덤으로 반환하는 함수"""
    top_20_songs = ranked_songs()[:20]
    recommend_songs = [song [0] for song in top_20_songs]
    return random.sample(recommend_songs, min(count, len(recommend_songs)))

def get_recommended_songs(user):
    """사용자의 추천 곡 리스트를 반환하는 함수"""
    
    # 1. 로그인 상태 확인
    if not user.is_authenticated:
        # 로그인하지 않은 사용자는 상위 20개의 랭킹 노래 중에서 4개를 랜덤으로 반환
        return get_random_ranking_songs()

    # 2. 로그인한 사용자의 구매 기록 확인
    filter_purchased = Order.objects.filter(user=user, payment__is_paid=True)
    purchased_songs = Song.objects.filter(id__in=filter_purchased.values('song_id')).distinct()
    
    if not purchased_songs.exists():
        # 구매한 노래가 없으면 상위 20개의 랭킹 노래 중에서 4개를 랜덤으로 반환
        return get_random_ranking_songs()

    # 3. 구매한 노래 기반 추천
    purchased_songs_genres = purchased_songs.values_list('genre', flat=True).distinct()
    purchased_songs_tempos = purchased_songs.values_list('tempo', flat=True).distinct()

    # 장르나 템포가 일치하는 노래를 추천
    recommended_songs = Song.objects.filter(genre__in=purchased_songs_genres).exclude(id__in=purchased_songs) | \
                        Song.objects.filter(tempo__in=purchased_songs_tempos).exclude(id__in=purchased_songs)
    recommended_songs = recommended_songs.distinct()

    if recommended_songs.exists():
        recommended_songs_list = list(recommended_songs)
        return random.sample(recommended_songs_list, min(4, len(recommended_songs_list)))
    
    # 4. 유사한 노래가 없으면 상위 20개의 랭킹 노래 중에서 4개를 랜덤으로 반환
    return get_random_ranking_songs()


# 홈 페이지 뷰
def home(request):
    """홈 페이지를 렌더링하는 함수"""
    songs = Song.objects.all().order_by('-created_at')[:4]  # 최근 노래 4개
    ranking_songs = ranked_songs()[:5]  # 랭킹 노래 5개
    form = SearchForm()

    # 추천 곡을 가져옵니다.
    recommended_songs = get_recommended_songs(request.user)

    context = {
        # 'object':songs,
        # 'ranking_songs':ranking_songs,
        # 'form':form,
        'object': songs,
        'ranking_songs': ranking_songs,
        'form': form,
        'recommended_songs': recommended_songs,
    }
    if recommended_songs:
        context['recommended_songs'] = recommended_songs
    return render(request, 'home.html', context)




def custom_404(request, exception):
    return render(request, '404.html', status=404)


def search(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        search_title = data.get('title')

        
        if ';' in search_title:
            parts = search_title.split(';')
            song_title = parts[0].strip()
            artist_name = parts[1].strip() if len(parts) > 1 else ''
            search_results = Song.objects.filter(title__icontains=song_title, seller__user__username__icontains=artist_name).distinct()
        elif len(search_title.strip()) == 0:
            search_results = None
        else:
            song_title = search_title
            search_results = Song.objects.filter(title__icontains=song_title).distinct()
        
        
        if search_results:
            search_html = "<ul class='search-results'>"
            for song in search_results:
                search_html += "<li class='search-item'>"
                search_html += "<a href='{}' class='text-decoration-none' >".format(reverse('songs:song_detail', args=[song.id]))
                search_html += "<img style='border: 1px solid hsla(0, 0%, 100%, .3);' src='{}' alt='{}' class='search-thumbnail'>".format(song.thumbnail.url, song.title)
                search_html += "<h1 class='fs-4 mt-2 mb-0 text-white'>{}</h1>".format(song.title)
                search_html += "<p class='text-black' ><a class='text-decoration-none' style='color:#888;' href='{}'>{}</a></p>".format(reverse('sellers:seller_artist', args=[song.seller.user.id]), song.seller)
                search_html += "</a>"
                search_html += "</li>"
            search_html += "</ul>"
            
            return JsonResponse({'success': 'true', 'data': search_html})
        else:
            return JsonResponse({'success': 'false', 'message': '검색 결과가 없습니다.'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

