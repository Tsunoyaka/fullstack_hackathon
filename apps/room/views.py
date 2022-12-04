from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from apps.hotel.permissions import IsOwner

from .serializers import RoomCreateSerializer, RoomSerializer
from .models import Room

class RoomView(CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RoomCRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminUser, IsOwner]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
