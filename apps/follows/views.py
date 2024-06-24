from django.shortcuts import render, get_object_or_404
from .models import Follows
from apps.songs.models import Song
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Follows
from .recommend import delete_cache, CACHE_KEY_USER_MATRIX, CACHE_KEY_USER_IDS, CACHE_KEY_KNN_MODEL
from django.http import JsonResponse

User = get_user_model()


@login_required
def follow_song(request, pk):

    following_user = get_object_or_404(Follows, pk=pk).following
    songs = Song.objects.filter(seller__user_id=following_user.pk).order_by(
        "-created_at"
    )

    paginator = Paginator(songs, 10)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)
    

    context = {
        "page_obj": page_obj,
        "page_range": page_range,
        "following_user": following_user,
        "songs": songs,
    }

    return render(request, "follows/following_song.html", context)

@login_required
def follow(request):
    user_id = request.GET.get("userid")
    try:
        user_to_follow = User.objects.get(pk=user_id)
        if request.user != user_to_follow:
            Follows.objects.get_or_create(follower=request.user, following=user_to_follow)
        return JsonResponse({"success": True})
    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "User does not exist"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def unfollow(request):
    user_id = request.GET.get("userid")
    try:
        user_to_unfollow = User.objects.get(pk=user_id)
        if request.user != user_to_unfollow:
            Follows.objects.filter(follower=request.user, following=user_to_unfollow).delete()
        return JsonResponse({"success": True})
    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "User does not exist"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})