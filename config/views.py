from django.shortcuts import render
from apps.songs.models import Song
# from apps.songs.models import Song

def home(request):
    
    # songs = Song.objects.all() 노래 가져오기 예시
    
    return render(request, 'home.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)