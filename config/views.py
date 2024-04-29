from django.shortcuts import render
from apps.songs.models import Song

# from apps.songs.models import Song

def home(request):
    
    songs = Song.objects.all()[:4] # 노래 가져오기 예시
    context = {
        'object':songs
    }
    return render(request, 'home.html',context)

def custom_404(request, exception):
    return render(request, '404.html', status=404)


from django.views.generic import FormView
from apps.songs.forms import PostSearchForm
from django.db.models import Q
#--- FormView
class SearchFormView(FormView): 
    form_class = PostSearchForm 
    template_name = 'search/post_search.html' 

    def form_valid(self, form):
        #검색어 확인
        searchWord = form.cleaned_data['search_word']
        #Q를 통해 검색하고
        post_list = Song.objects.filter(Q(title__icontains=searchWord)).distinct()
        #결과를 담아
        #페이지에 전달
        context = {} 
        context['form'] = form 
        context['search_term'] = searchWord 
        context['object_list'] = post_list 

        return render(self.request, self.template_name, context)