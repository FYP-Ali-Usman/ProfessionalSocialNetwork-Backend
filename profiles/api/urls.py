from django.conf.urls import url
from .views import ProfileApiView, ProfileApiView2
urlpatterns = [
    url(r'^$', ProfileApiView.as_view()),
    url(r'^u/$', ProfileApiView2.as_view()),
    # url(r'^create/$',StatusCreateApiView.as_view()),
    # url(r'^(?P<id>\d+)/$', StatusDetailApiView.as_view()),
    # url(r'^(?P<id>\d+)/update/$', StatusUpdateApiView.as_view()),
    # url(r'^(?P<id>\d+)/delete/$', StatusDeleteApiView.as_view()),
]
