from django.shortcuts import render
from apps.songs.models import Song
from django.http import JsonResponse
from config.forms import SearchForm
import json

def home(request):
    songs = Song.objects.all()[:4] # 노래 가져오기 예시
    form = SearchForm()
    context = {
        'object':songs,
        'form':form
    }
    return render(request, 'home.html',context)

def custom_404(request, exception):
    return render(request, '404.html', status=404)


def search(request):
    if request.method =='POST':
        data=json.loads(request.body.decode('utf-8'))
        
        name= data.get('name')
        
        return JsonResponse({'success':name})