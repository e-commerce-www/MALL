from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import JsonResponse, Http404
from apps.likes.models import Like
from apps.follows.models import Follows
from .models import Song
from .services import ranked_songs
import boto3
import os


def song_list(request):
    song_list = ranked_songs()
    paginator = Paginator(song_list, 5)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)

    return render(
        request,
        "songs/song_list.html",
        context={"page_obj": page_obj, "page_range": page_range},
    )


def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    like = None
    follow = None
    
    if request.user.is_authenticated:
        like = Like.objects.filter(user=request.user, song=song)
        follow = Follows.objects.filter(follower=request.user, following=song.seller.user)

    viewed_songs = request.session.get("viewed_songs", [])

    if song.id not in viewed_songs:
        viewed_songs.insert(0, song.id)
        viewed_songs = viewed_songs[:10]

    request.session["viewed_songs"] = viewed_songs
    
    disqus_short = f"{settings.DISQUS_SHORTNAME}"
    disqus_id = f"song-{song.seller}-{song.id}"
    disqus_url = f"{settings.DISQUS_MY_DOMAIN}{song.get_absolute_url()}"
    disqus_title = f"{song.title}-{song.seller}"
    
    context = {
        "song": song,
        'like': like,
        'follow': follow,
        "disqus_short": disqus_short,
        "disqus_id": disqus_id,
        "disqus_url": disqus_url,
        "disqus_title": disqus_title,
    }

    return render(request, "songs/song_detail.html", context=context)


def song_lyrics(request):
    song_id = request.GET.get("songid")
    if not song_id:
        return HttpResponse("Song ID not provided", status=400)
    try:
        song_lyrics = Song.objects.get(pk=song_id).lyrics
        if song_lyrics == '':
            song_lyrics = '가사가 없습니다.'
        return JsonResponse({"success": song_lyrics})
    except ObjectDoesNotExist:
        return HttpResponse("Song not found", status=404)
    except Exception as e:
        return HttpResponse(str(e), status=500)


def song_recent(request):
    songs = Song.objects.all().order_by("-created_at")
    page_number = request.GET.get("page", 1)
    paginator = Paginator(songs, 5)
    page_obj = paginator.get_page(page_number)
    return render(request, "songs/song_list_recent.html", {"page_obj": page_obj})


def song_ranking(request):
    songs = ranked_songs()
    paginator = Paginator(songs, 5)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)

    return render(
        request,
        "songs/song_list_ranking.html",
        context={"page_obj": page_obj, "page_range": page_range},
    )

# def song_genre(request):
#     genre = request.GET.get("genre")
#     if genre == "":
#         songs = Song.objects.all()
#     else:
#         songs = Song.objects.filter(genre=genre)
    
#     paginator = Paginator(songs, 5)

#     page_number = request.GET.get("page", 1)
#     page_obj = paginator.get_page(page_number)

#     current_page = page_obj.number
#     range_size = 5
#     half_range = range_size // 2

#     start_page = max(current_page - half_range, 1)
#     end_page = min(start_page + range_size - 1, paginator.num_pages)

#     page_range = range(start_page, end_page + 1)
    
#     return render(
#         request,
#         "songs/song_list_filters.html",
#         context={"page_obj": page_obj, "page_range": page_range},
#     )
    
# def song_tempo(request):
#     tempo = request.GET.get("tempo")
#     if tempo == "":
#         songs = Song.objects.all()
#     else:
#         songs = Song.objects.filter(tempo=tempo)

#     paginator = Paginator(songs, 10)

#     page_number = request.GET.get("page", 1)
#     page_obj = paginator.get_page(page_number)

#     current_page = page_obj.number
#     range_size = 5
#     half_range = range_size // 2

#     start_page = max(current_page - half_range, 1)
#     end_page = min(start_page + range_size - 1, paginator.num_pages)

#     page_range = range(start_page, end_page + 1)
    
#     return render(
#         request,
#         "songs/song_list_filters.html",
#         context={"page_obj": page_obj, "page_range": page_range},
#     )

def song_filter(request):
    tempo = request.GET.get("tempo", "")
    genre = request.GET.get("genre", "")

    songs = Song.objects.all()

    if genre:
        songs = songs.filter(genre=genre)

    if tempo:
        songs = songs.filter(tempo=tempo)

    paginator = Paginator(songs, 10)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)

    return render(
        request,
        "songs/song_list_filters.html",
        context={"page_obj": page_obj, "page_range": page_range,},
    )