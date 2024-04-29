from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from apps.songs.models import Song


def song_list(request):
    song_list = Song.objects.all()
    paginator = Paginator(song_list, 10)

    page_number = page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "songs/song_list.html", context={"page_obj": page_obj, "song_list" : song_list})


def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    
    viewed_songs = request.session.get('viewed_products', [])
    
    if song.id not in viewed_songs:
        viewed_songs.insert(0, song.id)
        viewed_songs = viewed_songs[:10]
    
    request.session['viewed_songs'] = viewed_songs

    return render(request, "songs/song_detail.html", context={"song": song})