from django.shortcuts import render
from django.urls import reverse
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
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        search_title = data.get('title')
        
        search_results = Song.objects.filter(title__icontains=search_title).distinct()
        if search_results:
            search_html = "<ul class='search-results'>"
            for song in search_results:
                search_html += "<li class='search-item'>"
                search_html += "<a href='{}'>".format(reverse('songs:song_detail', args=[song.id]))
                search_html += "<img src='{}' alt='{}' class='search-thumbnail'>".format(song.thumbnail.url, song.title)
                search_html += "<h3 class='search-title'>{}</h3>".format(song.title)
                search_html += "<p class='search-seller'>seller -  {}</p>".format(song.seller)
                search_html += "</a>"
                search_html += "</li>"
            search_html += "</ul>"
            
            return JsonResponse({'success': 'true', 'data': search_html})
        else:
            return JsonResponse({'success': 'false', 'message': '검색 결과가 없습니다.'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

      
# class SearchFormView(FormView): 
#     form_class = PostSearchForm 
#     template_name = 'search/post_search.html' 

#     def form_valid(self, form):
#         #검색어 확인
#         searchWord = form.cleaned_data['search_word']
#         #Q를 통해 검색하고
#         post_list = Song.objects.filter(Q(title__icontains=searchWord)).distinct()
#         #결과를 담아
#         #페이지에 전달
#         context = {} 
#         context['form'] = form 
#         context['search_term'] = searchWord
#         context['object_list'] = post_list 

#         return render(self.request, self.template_name, context)

