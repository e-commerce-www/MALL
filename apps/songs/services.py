import math
from django.utils import timezone
from .models import Song
from apps.likes.models import Like


def decayed_likes_count(song, halflife=48):
    now = timezone.now()
    likes = Like.objects.filter(song=song)
    decayed_count = 0.0
    for like in likes:
        hours_passed = (now - like.created_at).total_seconds() / 3600
        decayed_count += 0.5 ** (hours_passed / halflife)
    return decayed_count

def ranked_songs():
    songs = Song.objects.all()
    songs_with_decayed_likes = [(song, decayed_likes_count(song)) for song in songs]
    return sorted(songs_with_decayed_likes, key=lambda x: x[1], reverse=True)

