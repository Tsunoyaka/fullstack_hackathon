from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import HotelListViewSet
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register('post', HotelListViewSet, 'post')
# router.register('comment', CommentCreateDeleteView)
# router.register('tags', TagViewSet, 'tags')

urlpatterns = [
    # path('list/', HotelListViewSet.as_view(), name='hotel_list')
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    