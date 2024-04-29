from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from apps.songs.models import Song


def song_list(request):
    song_list = Song.objects.all()
    paginator = Paginator(song_list, 10)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)

    return render(request, "songs/song_list.html", context={"page_obj": page_obj, 'page_range': page_range})


def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    
    viewed_songs = request.session.get('viewed_songs', [])
    
    if song.id not in viewed_songs:
        viewed_songs.insert(0, song.id)
        viewed_songs = viewed_songs[:10]
    
    request.session['viewed_songs'] = viewed_songs

    return render(request, "songs/song_detail.html", context={"song": song})