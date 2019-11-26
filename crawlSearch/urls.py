from django.conf.urls import url
from .views import Favourites,AuthorSearch,AfterCrawlSearch,PublSearch,onePublSearch,OneAuthorSearch,CoautherSearch
urlpatterns = [
    url(r'^authSearch/$', AuthorSearch.as_view()),
    url(r'^apubSearch/$', PublSearch.as_view()),
    url(r'^oneSearch/$', OneAuthorSearch.as_view()),
    url(r'^coauth/$', CoautherSearch.as_view()),
    url(r'^authSearchYeild/$', AfterCrawlSearch.as_view()),
    url(r'^onePub/$', onePublSearch.as_view()),
    url(r'^fav/$', Favourites.as_view()),
]