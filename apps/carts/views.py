from django.shortcuts import render, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Cart

@login_required
def my_songs(request):
    my_song = get_list_or_404(Cart, user=request.user)
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
