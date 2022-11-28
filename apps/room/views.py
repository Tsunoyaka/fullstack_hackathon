from rest_framework import generics
from .serializers import RoomListSerializer, RoomCRUDSerializer
from .models import Room


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer


class RoomRetrieveView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCRUDSerializer


class RoomCreateView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCRUDSerializer


class RoomUpdateView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCRUDSerializer


class RoomDeleteView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCRUDSerializer  