from django import forms
from .models import Song

class PostSearchForm(forms.Form):
    search_word=forms.CharField(label='Search Word')
    
class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'genre', 'tempo', 'thumbnail', 'mp3', 'lyrics']
        labels = {
            'title': '타이틀',
            'genre': '장르',
            'tempo': '템포',
            'thumbnail': '썸네일',
            'mp3': '음원 파일 [.mp3 파일]',
            'lyrics': '가사 [옵션]',
        }
        

class SongEditForm(forms.ModelForm):
        class Meta:
            model = Song
            fields = ['title', 'genre', 'tempo', 'thumbnail', 'mp3', 'lyrics']
            labels = {
                'title': '타이틀',
                'genre': '장르',
                'tempo': '템포',
                'thumbnail': '썸네일',
                'mp3': '음원 파일 [.mp3 파일]',
                'lyrics': '가사 [옵션]',
            }
    