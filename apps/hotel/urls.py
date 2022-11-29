from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import HotelListViewSet


router = DefaultRouter()
router.register('hotels', HotelListViewSet, 'hotel')
# router.register('comments', CommentCreateDeleteView, 'hotel')
# router.register('tags', TagViewSet, 'tags')

urlpatterns = [
    # path('list/', HotelListViewSet.as_view(), name='hotel_list')
]

urlpatterns += router.urls