"""testapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf.urls import url
from django.views.static import serve
from . import settings

router = routers.DefaultRouter()
# router.register(r'bigsearch', views.URLViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #TODO path needs to be changed in the frontend too.
    path('main/', include('main.urls')),

    path('profile/', include('profiles.api.urls')),
    path('api/auth/', include('accounts.api.urls')),
    path('scrape/', include('scrape.urls')),
    path('forum/', include('forum.api.urls')),
    path('search/', include('crawlSearch.urls')),
    path('graph/', include('graph.urls')),

    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]