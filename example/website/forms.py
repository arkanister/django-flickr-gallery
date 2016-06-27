from ckeditor.widgets import CKEditorWidget
from django import forms

from example.website.models import Article


class ArticleAdminForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'content': CKEditorWidget
        }
