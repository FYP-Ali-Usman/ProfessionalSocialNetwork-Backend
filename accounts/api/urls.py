from django.conf.urls import url
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import AuthView, RegisterAPIView,UserApiView

urlpatterns = [
    url(r'^$', AuthView.as_view()),
    url(r'^register/$', RegisterAPIView.as_view()),
    url(r'^update/$', UserApiView.as_view()),
    url(r'^jwt/', obtain_jwt_token),
    url(r'^jwt/refresh/', refresh_jwt_token),
    ]
