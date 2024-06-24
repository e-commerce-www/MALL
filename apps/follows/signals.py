from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Follows
from config.cache_utils import delete_cache
from .recommend import CACHE_KEY_USER_MATRIX, CACHE_KEY_USER_IDS, CACHE_KEY_KNN_MODEL

@receiver(post_save, sender=Follows)
@receiver(post_delete, sender=Follows)
def clear_cache(sender, **kwargs):
    # print("Clearing cache due to Follows model change")
    delete_cache(CACHE_KEY_USER_MATRIX)
    delete_cache(CACHE_KEY_USER_IDS)
    delete_cache(CACHE_KEY_KNN_MODEL)
