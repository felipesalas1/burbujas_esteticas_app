from django.urls import path
from .views import RoomCreate, RoomView

urlpatterns = [
    path('', RoomView.as_view()),
    path('create', RoomCreate.as_view())
]