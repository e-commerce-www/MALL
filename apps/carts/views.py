from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Cart
from django.http import JsonResponse
from apps.songs.models import Song

@login_required
def my_songs(request):
    my_song = Cart.objects.all()
    paginator = Paginator(my_song, 10)
    
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)
    
    return render(request, 'carts/my_songs.html', context={'page_obj': page_obj, 'page_range': page_range})

@login_required
def add_song(request):
    song_id = request.GET.get('songid')
    song = Song.objects.get(pk=song_id)
    cart = Cart.objects.get_or_create(
        user=request.user,
        song=song
    )
    return JsonResponse({'success': song.title, 'song_id': song_id})

@login_required
def remove_song(request):
    song_id = request.GET.get('songid')
    cart_item = get_object_or_404(Cart, song__id=song_id, user=request.user)
    cart_item.delete()

    return JsonResponse({'success': '찜 목록에서 제거되었습니다.', 'song_id': song_id})