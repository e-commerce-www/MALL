from django.shortcuts import render
from django.urls import reverse
from apps.songs.models import Song
from django.http import JsonResponse
from config.forms import SearchForm
from apps.songs.services import ranked_songs
import json

def home(request):
    songs = Song.objects.all()[:4] # 노래 가져오기 예시
    ranking_songs = ranked_songs()
    form = SearchForm()
    context = {
        'object':songs,
        'ranking_songs':ranking_songs,
        'form':form
    }
    return render(request, 'home.html', context)


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def search(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        search_title = data.get('title')
        
        search_results = Song.objects.filter(title__icontains=search_title).distinct()
        if search_results:
            search_html = "<ul class='search-results'>"
            for song in search_results:
                search_html += "<li class='search-item'>"
                search_html += "<a href='{}'>".format(reverse('songs:song_detail', args=[song.id]))
                search_html += "<img src='{}' alt='{}' class='search-thumbnail'>".format(song.thumbnail.url, song.title)
                search_html += "<h3 class='search-title'>{}</h3>".format(song.title)
                search_html += "<p class='search-seller'>seller -  {}</p>".format(song.seller)
                search_html += "</a>"
                search_html += "</li>"
            search_html += "</ul>"
            
            return JsonResponse({'success': 'true', 'data': search_html})
        else:
            return JsonResponse({'success': 'false', 'message': '검색 결과가 없습니다.'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def daily_chart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            search_html = "<h3>hello</h3>"
            return JsonResponse({'message': 'hi', 'data': search_html})
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'})
