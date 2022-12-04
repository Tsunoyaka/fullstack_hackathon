from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import RoomCRUDView, RoomView

urlpatterns = [
    path('add-room/', RoomView.as_view()),
    path('crud-room/<str:pk>/', RoomCRUDView.as_view())
]
