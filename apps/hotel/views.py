from urllib.request import Request
from django_filters import rest_framework as rest_filter
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.decorators import method_decorator

from .serializers import HotelListSerializer, HotelCreateSerializer, HotelSerializer
from .models import Hotel
from .permissions import IsOwner

class PriceFilter(rest_filter.FilterSet):
    max_price = rest_filter.NumberFilter(field_name="room_manager__room_price", lookup_expr='lt')
    min_price = rest_filter.NumberFilter(field_name="room_manager__room_price", lookup_expr='gt')

    class Meta:
        model = Hotel
        fields = ['region', 'stars']




class HotelListViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializer
    filter_backends = [
        filters.SearchFilter, 
        rest_filter.DjangoFilterBackend, 
        filters.OrderingFilter]
    search_fields = ['title','stars']
    filterset_fields = ['pets', 'food', 'region']
    ordering_fields = ['room_manager__room_price']
    range_fields = ['room_manager__room_price']
    filterset_class = PriceFilter

    @method_decorator(cache_page(60*15 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()
