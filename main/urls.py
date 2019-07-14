from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #TODO allow people to update their organization or other things in profile incase if organization was changed or was not previously in the database

    path('', views.index, name = 'index'),
]