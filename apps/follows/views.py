from django.shortcuts import render, get_object_or_404
from . models import Follows
from apps.songs.models import Song
from django.core.paginator import Paginator



# Create your views here.
def follow_song(request, pk):

    following_user = get_object_or_404(Follows, pk=pk).following
    songs = Song.objects.filter(seller__user_id = following_user.pk).order_by('-created_at')

    paginator = Paginator(songs, 3)

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
        'following_user':following_user,
        'songs':songs
    }

    
    return render(request, 'follows/following_song.html', context)

def add_follow(request):
    pass