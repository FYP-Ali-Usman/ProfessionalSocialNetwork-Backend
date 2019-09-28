from django.contrib import admin
from .models import Article,Comment #,Tag
from .forms import ArticleForm,CommentForm #,TagForm

# Register your models here.
# class TagAdmin(admin.ModelAdmin):
#     list_display = ['tag','searc_frequency']
#     form = TagForm

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['user','title','discription','image','tags','favourites','Updated_at']
    form = ArticleForm
    # class Meta:
    #     # model = Status
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','image','article','body','Updated_at']
    form = CommentForm


# admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)