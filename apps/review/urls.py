from django.urls import path

from .views import CreateCommentView, DesUpdCommentView, DislikeView, LikeView

urlpatterns = [
    path('add-comment/', CreateCommentView.as_view(), name='create_com'),
    path('upd-del-comment/<int:pk>/', DesUpdCommentView.as_view()),
    path('like/', LikeView.as_view()),
    path('dislike/', DislikeView.as_view()),
]