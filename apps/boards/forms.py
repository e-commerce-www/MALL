from django import forms
from .models import Board, Reply

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["title", "content"]
        labels = {
            "title" : "제목",
            "content" : "내용",
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["content"]
        labels = {
            "content" : "내용",
        }