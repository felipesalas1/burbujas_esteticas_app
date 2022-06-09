from django.urls import path, include
from .views import index

app_name = 'frontend'

urlpatterns = [
    path('', index),
    path('app', index),
    path('create', index),
]