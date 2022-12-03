from django.urls import path

from .views import CreateComment, DesUpdComment

urlpatterns = [
    path('add_comment/<str:slug>/', CreateComment.as_view()),
    path('del_comment/<str:slug>/<int:pk>/', DesUpdComment.as_view()),
    path('upd_comment/<str:slug>/<int:pk>/', DesUpdComment.as_view()),
]