from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Like
from apps.songs.models import Song
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

