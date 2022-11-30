from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views import ListView

router = DefaultRouter()
router.register('bookings', ListView, 'booking')