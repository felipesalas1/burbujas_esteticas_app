from django.contrib import admin
from django.urls import include, path

from spotify.views import spotify_callback
from .views import AuthURL, createplaylist, spotify_callback, IsAuthenticated, GetSessionid


''''
Vincula las urls del back con las funciones en Util.py y Views.py
'''

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_callback),
    path('is-authenticated', IsAuthenticated.as_view()),
    path('createplaylist', createplaylist.as_view()),
    path('getsessionid', GetSessionid.as_view()),
]
