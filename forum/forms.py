from django import forms
from .models import Article as ArticleModel
from .models import Comment as CommentModel
# from .models import Tag as TagModel

# class TagForm(forms.ModelForm):
#     class Meta:
#         model = TagModel
#         fields = '__all__'
    
#     def clean_body(self, *args, **kwargs):
#         tag = self.cleaned_data.get('tag')
#         if len(tag) > 50:
#             raise forms.ValidationError("Tag name is too long")
#         return tag

class ArticleForm(forms.ModelForm):
    class Meta:
        model = ArticleModel
        fields = '__all__'
    
    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        if len(title) > 150:
            raise forms.ValidationError('Title name is too long')
        return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = '__all__'
    
    def clean_body(self, *args, **kwargs):
        body = self.cleaned_data.get('body')
        if body=="":
            raise forms.ValidationError("Body can't be empty")
        return body