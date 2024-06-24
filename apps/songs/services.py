import math
from django.utils import timezone
from .models import Song
from apps.likes.models import Like
from config.cache_utils import set_cache, get_cache, delete_cache

CACHE_KEY_RANKED_SONGS = 'ranked_songs'
CACHE_KEY_RECENT_SONGS = 'recent_songs'

def decayed_likes_count(song, halflife=48):
    now = timezone.now()
    likes = Like.objects.filter(song=song)
    decayed_count = 0.0
    for like in likes:
        hours_passed = (now - like.created_at).total_seconds() / 3600
        decayed_count += 0.5 ** (hours_passed / halflife)
    return decayed_count

def ranked_songs():
    cached_songs = get_cache(CACHE_KEY_RANKED_SONGS)
    if cached_songs is not None:
        return cached_songs
    
    songs = Song.objects.all()
    songs_with_decayed_likes = [(song, decayed_likes_count(song)) for song in songs]
    sorted_songs = sorted(songs_with_decayed_likes, key=lambda x: x[1], reverse=True)

    set_cache(CACHE_KEY_RANKED_SONGS, sorted_songs, timeout=3600)
    return sorted_songs

def recent_songs():
    cached_songs = get_cache(CACHE_KEY_RECENT_SONGS)
    if cached_songs is not None:
        return cached_songs

    songs = Song.objects.all().order_by("-created_at")
    set_cache(CACHE_KEY_RECENT_SONGS, songs, timeout=3600)
    return songs

