from django.shortcuts import render, get_object_or_404
from . models import Follows
from apps.songs.models import Song
from apps.oauth.models import User



# Create your views here.
def follow_song(request, pk):

    following_user = get_object_or_404(Follows, pk=pk).following
    songs = Song.objects.filter(seller__user_id = following_user.pk)

    
    return render(request, 'follows/following_song.html', context= {'following_user':following_user,'songs':songs})
