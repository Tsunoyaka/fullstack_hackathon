from rest_framework import fields, serializers

from apps.account.models import User
from apps.hotel.serializers import HotelSerializer
from apps.room.serializers import RoomCRUDSerializer
from .models import Booking 


class GuestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = User
        fields = ("username", "email")
        

class BookingSerializer(serializers.ModelSerializer):
    user = User
    hotel = HotelSerializer
    room  = RoomCRUDSerializer
    class Meta:
        model = Booking
        fields =("username", "hotel", "room", "checkin_date", "checkout_date", "charge",)
