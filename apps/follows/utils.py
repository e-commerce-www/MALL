import pandas as pd
import pickle
from django.core.cache import cache
from django.conf import settings
from sklearn.neighbors import NearestNeighbors
from django.contrib.auth import get_user_model
from apps.follows.models import Follows

User = get_user_model()
CACHE_KEY_USER_MATRIX = 'user_follow_matrix'
CACHE_KEY_USER_IDS = 'user_ids'
CACHE_KEY_KNN_MODEL = 'knn_model'


def set_cache(key, value, timeout=settings.CACHE_TIMEOUT):
    cache.set(key, pickle.dumps(value), timeout)


def get_cache(key):
    value = cache.get(key)
    return pickle.loads(value) if value else None


def delete_cache(key):
    cache.delete(key)
    

def prepare_follow_matrix():
    cached_matrix = get_cache(CACHE_KEY_USER_MATRIX)
    cached_user_ids = get_cache(CACHE_KEY_USER_IDS)

    if cached_matrix is not None and cached_user_ids is not None:
        return cached_matrix, cached_user_ids

    follows = Follows.objects.all().values('follower_id', 'following_id')
    if not follows:
        return pd.DataFrame(), []

    df = pd.DataFrame(list(follows))
    user_ids = list(User.objects.values_list('id', flat=True))

    user_follow_matrix = pd.crosstab(df['follower_id'], df['following_id']).reindex(index=user_ids, columns=user_ids, fill_value=0)

    set_cache(CACHE_KEY_USER_MATRIX, user_follow_matrix)
    set_cache(CACHE_KEY_USER_IDS, user_ids)

    return user_follow_matrix, user_ids


def train_knn_model(user_follow_matrix):
    cached_knn = get_cache(CACHE_KEY_KNN_MODEL)

    if cached_knn is not None:
        return cached_knn

    if user_follow_matrix.empty or len(user_follow_matrix) < 2:
        return None

    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(user_follow_matrix)

    set_cache(CACHE_KEY_KNN_MODEL, knn)

    return knn


def recommend_follows_knn(user_id, knn, user_follow_matrix, user_ids, top_n=5):
    if knn is None or user_id not in user_ids:
        return []

    user_vector = user_follow_matrix.loc[user_id].values.reshape(1, -1)
    n_neighbors = min(top_n + 1, len(user_follow_matrix))

    if n_neighbors <= 1:
        return []

    distances, indices = knn.kneighbors(user_vector, n_neighbors=n_neighbors)

    similar_indices = indices.flatten()[1:]  # 첫 번째 인덱스는 자기 자신이므로 제외
    similar_users = [user_ids[idx] for idx in similar_indices]


    followed_users = set(user_follow_matrix.columns[user_follow_matrix.loc[user_id] == 1]) # 사용자 이미 팔로우한 사용자 집합
    recommendations = set()

    for similar_user in similar_users:
        similar_user_followings = set(user_follow_matrix.columns[user_follow_matrix.loc[similar_user] == 1])
        
        # 사용자와 유사한 사용자의 팔로우 목록이 겹치는지 확인
        if followed_users & similar_user_followings:
            recommendations.update(similar_user_followings - followed_users)

    return list(recommendations)[:top_n]
