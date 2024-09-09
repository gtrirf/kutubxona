from django import forms
from .models import Post, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'image': 'Image',
            'body': 'Content',
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'comment': 'Comment',
        }

