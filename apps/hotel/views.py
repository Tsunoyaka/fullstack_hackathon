from django_filters import rest_framework as rest_filter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import filters, status, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.review.serializers import CommentSerializer
from .serializers import HotelListSerializer, HotelCreateSerializer, HotelSerializer
from .models import Hotel
from .permissions import IsOwner


class HotelListViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializer
    filter_backends = [
        filters.SearchFilter, 
        rest_filter.DjangoFilterBackend, 
        filters.OrderingFilter]
    search_fields = ['title','stars']
    filterset_fields = ['pets', 'food']

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return HotelListSerializer
        elif self.action == 'create':
            return HotelCreateSerializer
        elif self.action == 'retrieve':
            return HotelSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action == 'comment' and self.request.method == 'DELETE':
            self.permission_classes = [IsOwner]
        if self.action in ['create', 'comment', 'set_rating', 'like']:
            self.permission_classes = [IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=True, methods=['POST', 'DELETE'])
    def comment(self, request, pk=None):
        hotel = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, hotel=hotel)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )

