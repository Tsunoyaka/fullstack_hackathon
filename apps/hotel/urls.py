from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import HotelListViewSet


router = DefaultRouter()
router.register('hotels', HotelListViewSet, 'hotel')


urlpatterns = [

]

urlpatterns += router.urls

