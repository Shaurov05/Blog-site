from django import forms
from . models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        fields = ("title","message", "category")
        model  = Post

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'message':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
