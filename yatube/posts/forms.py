from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Введите текст',
            'group': 'Выберите группу',
            'image': 'Загрузить картинку'
        }
        help_texts = {
            'text': 'Хоть что-то :(',
            'group': 'Из существующих',
            'image': 'Кто сфоткал?'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
