from django.forms import ModelForm, Textarea
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {'content': 'New Post'}
        widgets = {
            'content': Textarea(attrs={'class': 'form-control mb-1', 'rows': '2'})
        }
