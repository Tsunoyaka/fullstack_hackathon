from django.urls import path
from .views import (
    RoomCreateView,
    RoomDeleteView,
    RoomListView,
    RoomUpdateView,
    RoomRetrieveView
    )


urlpatterns = [
    path('all/', RoomListView.as_view()),
    path('create/', RoomCreateView.as_view(), name='create'),
    path('delete/', RoomDeleteView.as_view(), name='delete'),
    path('retrieve/', RoomRetrieveView.as_view(), name='detail'),
    path('update/', RoomUpdateView.as_view(), name='update')
]


