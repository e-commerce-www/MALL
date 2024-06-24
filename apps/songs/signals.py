from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.likes.models import Like
from config.cache_utils import delete_cache
from .services import CACHE_KEY_RANKED_SONGS, CACHE_KEY_RECENT_SONGS
from .models import Song

@receiver(post_save, sender=Like)
@receiver(post_delete, sender=Like)
def clear_cache_on_like_change(sender, instance, **kwargs):
    delete_cache(CACHE_KEY_RANKED_SONGS)

@receiver(post_save, sender=Song)
@receiver(post_delete, sender=Song)
def clear_cache_on_song_change(sender, instance, **kwargs):
    delete_cache(CACHE_KEY_RECENT_SONGS)
