from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
# from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from rest_framework.views import APIView
from .serializers import LikeSerializer, DislikeSerializer

from rest_framework.request import Request

from .serializers import CommentCRUDSerializer, CommentDelUpdSerializer
from .models import Comment
from .permissions import IsOwner
from apps.hotel.models import Hotel


class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=CommentCRUDSerializer)
    def post(self, request: Request):
        serializer = CommentCRUDSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response('Comment Created!')



class DesUpdCommentView(APIView):
    permission_classes = [IsAdminUser, IsOwner]
    
    def delete(self, request, pk):
        obj = Comment.objects.get(pk=pk)
        serializer = CommentDelUpdSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.delete()
            return Response('Comment deleted!')

    @swagger_auto_schema(request_body=CommentDelUpdSerializer)
    def put(self, request, pk):
        try:
            instance = Comment.objects.get(pk=pk)
            serailizer = CommentDelUpdSerializer(data=request.data, instance=instance, context={'request': request})
            if serailizer.is_valid(raise_exception=True):            
                serailizer.save()  
            return Response('Комментарий успешно изменен')
        except Comment.DoesNotExist:
            return Response('Страница не найдена!', status=status.HTTP_404_NOT_FOUND)


class LikeView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=LikeSerializer)
    def post(self, request):
        serializer = LikeSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response('Liked!')

    @swagger_auto_schema(request_body=LikeSerializer)
    def delete(self, request):
        serializer = LikeSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.unlike()
            return Response('Unliked!')


class DislikeView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=DislikeSerializer)
    def post(self, request):
        serializer = DislikeSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response('Disiked!')

    @swagger_auto_schema(request_body=DislikeSerializer)
    def delete(self, request):
        serializer = DislikeSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.undislike()
            return Response('Undisliked!')

