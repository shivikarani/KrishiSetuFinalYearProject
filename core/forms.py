from django import forms
from .models import Query, QueryMedia

class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['title', 'description', 'crop']

class QueryMediaForm(forms.ModelForm):
    class Meta:
        model = QueryMedia
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(),  # no 'multiple' here
        }

from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'crop']
