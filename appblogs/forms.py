from django import forms
from .models import Blog, Post

class FormBlog(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["nome","descricao","tema"]


class FormPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo","resumo","conteudo"]