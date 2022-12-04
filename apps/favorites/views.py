from urllib.request import Request
from requests import delete
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as rest_filter
from apps.review.permissions import IsOwner
from rest_framework.generics import ListAPIView
from .serializers import FavoritesSerializer
from .models import Favorites


class FavoritesView(APIView): 
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=FavoritesSerializer)
    def post(self, request):
        serializer = FavoritesSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response('Favorites!')

    # def delete(self, request):
    #     serializer = FavoritesSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.

