from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import HotelListViewSet


router = DefaultRouter()
router.register('hotels', HotelListViewSet, 'hotel')


urlpatterns = [
    # path("hotels/<str:slug>/delete_comment/<int:pk>", DeleteUpdateCommentApiView.as_view(), name='delete_comment'),
    # path("hotels/<str:slug>/update_comment/<int:pk>", DeleteUpdateCommentApiView.as_view(), name='update_comment')
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    