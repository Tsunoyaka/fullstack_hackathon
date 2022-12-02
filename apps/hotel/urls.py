from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import HotelListViewSet, DeleteCommentApiView


router = DefaultRouter()
router.register('hotels', HotelListViewSet, 'hotel')


urlpatterns = [
    # path('list/', HotelListViewSet.as_view(), name='hotel_list')
    path("hotels/<str:slug>/delete_comment/<int:pk>", DeleteCommentApiView.as_view(), name='delete_comment')
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    