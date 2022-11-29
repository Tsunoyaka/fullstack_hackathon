from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as rest_filter
from .serializers import HotelListSerializer
from .models import Hotel
from rest_framework import filters


class HotelListViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializer
    filter_backends = [
        filters.SearchFilter, 
        rest_filter.DjangoFilterBackend, 
        filters.OrderingFilter]