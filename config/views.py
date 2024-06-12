from django.shortcuts import render
from django.urls import reverse
from apps.songs.models import Song
from django.http import JsonResponse
from config.forms import SearchForm
from apps.songs.services import ranked_songs
from apps.carts.models import Cart
import json

def song_recommend(user):
    # 사용자의 카트에 담긴 노래 가져오기
    user_cart_songs = Cart.objects.filter(user=user)
    
    # 사용자가 카트에 담은 노래의 ID를 가져오기
    user_song_ids = user_cart_songs.values_list('song_id', flat=True)
    
    # 카트에 담긴 노래와 같은 장르의 다른 노래 추천 (예시)
    recommended_songs = Song.objects.filter(genre__in=Song.objects.filter(id__in=user_song_ids).values_list('genre', flat=True)).exclude(id__in=user_song_ids).order_by('?')[:4]
    
    return recommended_songs


def home(request):
    songs = Song.objects.all().order_by('-created_at')[:5] # 노래 가져오기 예시
    ranking_songs = ranked_songs()[:5]
    user_cart_songs = Cart.objects.filter(user=request.user)
    recommended_songs = song_recommend(request.user)
    form = SearchForm()
    context = {
        'object':songs,
        'ranking_songs':ranking_songs,
        'form':form,
        'recommended_songs': recommended_songs  # 추천 노래 목록 템플릿에 전달
    }
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

