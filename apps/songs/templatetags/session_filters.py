from django import template
from apps.songs.models import Song

register = template.Library()

@register.filter
def get_song(song_id):
    return Song.objects.get(id=song_id)