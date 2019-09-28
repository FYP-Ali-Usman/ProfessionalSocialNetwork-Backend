from django.conf.urls import url
from .views import AuthorSearch,PublSearch,OneAuthorSearch
urlpatterns = [
    url(r'^authSearch/$', AuthorSearch.as_view()),
    url(r'^apubSearch/$', PublSearch.as_view()),
    url(r'^oneSearch/$', OneAuthorSearch.as_view()),
]