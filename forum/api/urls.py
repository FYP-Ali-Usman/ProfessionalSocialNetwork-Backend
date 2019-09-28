from django.conf.urls import url
from .views import ArticleApiView,ArticleDetailApiView,CommentApiView,CommentDetailApiView
urlpatterns = [
    url(r'^article/$', ArticleApiView.as_view()),
    url(r'^article/ui$', ArticleDetailApiView.as_view()),
    url(r'^comment/$', CommentApiView.as_view()),
    url(r'^comment/ui$', CommentDetailApiView.as_view()),
    # url(r'^u/$', ProfileApiView2.as_view()),
    # url(r'^create/$',StatusCreateApiView.as_view()),
    # url(r'^(?P<id>\d+)/$', StatusDetailApiView.as_view()),
    # url(r'^(?P<id>\d+)/update/$', StatusUpdateApiView.as_view()),
    # url(r'^(?P<id>\d+)/delete/$', StatusDeleteApiView.as_view()),
]
