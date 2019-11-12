from django.urls import path
from recommends import views
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', csrf_exempt(views.recommend)),
    url(r'^advance/$', views.RecommendSearch.as_view())
    
]