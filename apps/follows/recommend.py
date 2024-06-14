import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth import get_user_model
from .models import Follows

User = get_user_model()

def get_follow_matrix():
    users = User.objects.all()
    user_ids = np.array([users.id for user in users])
    follow_matrix = np.zeros((len(user_ids), len(user_ids)))

    for follow in Follows.objects.all():
        pass
    pass