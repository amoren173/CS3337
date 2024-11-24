from django import forms
from django.forms import ModelForm
from .models import Book
from .models import messageboard



class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


