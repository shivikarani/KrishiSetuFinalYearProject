from django import forms
from .models import Query, QueryMedia

class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['title', 'description', 'crop']

class QueryMediaForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = QueryMedia
        fields = ['file']


from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'crop']
