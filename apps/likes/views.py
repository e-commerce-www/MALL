from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Like, BoardLike, Bookmark
from apps.songs.models import Song
from apps.boards.models import Board
from django.http import JsonResponse
# Create your views here.

@login_required
def like_do(request):
    song_id = request.GET.get("songid")
    like = Like.objects.get_or_create(
        song=Song.objects.get(pk=song_id),
        user=request.user
    )
    
    return JsonResponse({'success': True})

@login_required
def like_cancel(request):
    song_id = request.GET.get("songid")
    like = Like.objects.get(user=request.user, song=Song.objects.get(pk=song_id))
    like.delete()
    
    return JsonResponse({'success': True})

def board_like_do(request):
    board_id = request.GET.get("boardid")
    board = get_object_or_404(Board, pk=board_id)
    board_like, created = BoardLike.objects.get_or_create(
        user = request.user,
        board = board
    )

    if not created:
        board_like.delete()
        return JsonResponse({'success': True, 'liked': False})

    return JsonResponse({'success': True, 'liked': True})

def bookmark_do(request):
    board_id = request.GET.get("boardid")
    board = get_object_or_404(Board, pk=board_id)
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user, 
        board=board
    )

    if not created:
        bookmark.delete()
        return JsonResponse({'success': True, 'bookmarked': False})

    return JsonResponse({'success': True, 'bookmarked': True})