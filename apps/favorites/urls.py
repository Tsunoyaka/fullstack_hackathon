from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

from .views import FavoritesView




urlpatterns = [
    path('add-favorite/', FavoritesView.as_view()),
]
