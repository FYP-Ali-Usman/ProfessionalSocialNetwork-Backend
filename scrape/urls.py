from django.urls import path
from scrape import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
#    path('', views.index, name = 'index'),

    # TODO arrange following 2 paths to scrap/big and scrap/advanced while scrap in main(testapi) view from where big and advanced divided to the respective scrap application views.py
    path('bigsearch', csrf_exempt(views.search_faculty)),
    path('singleSearch', csrf_exempt(views.search_author)),
    path('advancedsearch', csrf_exempt(views.search_advanced_faculty)),
]