import pickle
from django.core.cache import cache
from django.conf import settings

def set_cache(key, value, timeout=settings.CACHE_TIMEOUT):
    cache.set(key, pickle.dumps(value), timeout)

def get_cache(key):
    value = cache.get(key)
    return pickle.loads(value) if value else None

def delete_cache(key):
    cache.delete(key)