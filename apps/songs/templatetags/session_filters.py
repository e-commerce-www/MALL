from django import template
from apps.songs.models import Song
from apps.orders.models import Order
from apps.carts.models import Cart

register = template.Library()

# @register.filter
# def get_song(song_id):
#     return Song.objects.get(id=song_id)

@register.filter
def get_song(song_id):
    try:
        return Song.objects.get(id=song_id)
    except Song.DoesNotExist:
        return None

@register.simple_tag
def is_purchased(user, song_id):
    return Order.objects.filter(user=user, payment__is_paid=True, song__id=song_id).exists()

@register.simple_tag
def is_added_to_cart(user, song_id):
    return Cart.objects.filter(user=user, song__id=song_id).exists()