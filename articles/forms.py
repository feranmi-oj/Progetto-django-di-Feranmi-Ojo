from django import forms

from .models import Article

class ArticleEditForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title','category','img', 'content',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'img': forms.FileInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }