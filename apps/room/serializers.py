from rest_framework import serializers
from .models import Room


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('room_title', 'room_type', 'room_price')


class RoomCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'