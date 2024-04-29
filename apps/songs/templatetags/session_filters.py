from django import template
from apps.songs.models import Song
from apps.orders.models import Order
from django.contrib.auth import get_user_model

register = template.Library()

@register.filter
def get_song(song_id):
    return Song.objects.get(id=song_id)

@register.simple_tag
def is_purchased(user, song_id):
    return Order.objects.filter(user=user, payment__is_paid=True, song__id=song_id).exists()