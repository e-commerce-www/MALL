from django.shortcuts import render, get_object_or_404
from . models import Follows
from apps.songs.models import Song
from apps.sellers.models import Seller



# Create your views here.
def follow_song(request, pk):
    follow = get_object_or_404(Follows, pk=pk)
    song = get_object_or_404(Song, pk=pk)

    following_user = Follows.objects.filter(follower= request.user).values('following')
    songs = Song.objects.filter(seller__user_id__in = following_user)

    

    return render(request, 'follows/following_song.html', context= {'follow': follow , 'songs':songs})
