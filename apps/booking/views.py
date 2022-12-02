from rest_framework import status
from rest_framework.viewsets import ModelViewSet 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from collections import namedtuple

from .models import Booking
from .serializers import GuestSerializer, BookingSerializer
from apps.room.models import Room
from apps.hotel.models import Hotel
from apps.account.models import User 
from apps.hotel.serializers import HotelSerializer
from apps.room.serializers import RoomCRUDSerializer 


nt = namedtuple("object", ["model", "serializers"])
pattern = {
    "username"  : nt(User, GuestSerializer),
    "hotel"  : nt(Hotel, HotelSerializer),
    "room"   : nt(Room, RoomCRUDSerializer),
    "booking": nt(Booking, BookingSerializer),
}


@api_view(["GET", "POST"])
def ListView(request, api_name):
    object =  pattern.get(api_name, None)
    if object == None:
        return Response(
            data   = "Invalid URL",
            status = status.HTTP_404_NOT_FOUND,
        )
    if request.method == "GET":
        object_list = object.model.objects.all()
        serializers  = object.serializers(object_list, many=True)
        return Response(serializers.data)

    if request.method == "POST":
        data = request.data
        serializers = object.serializers(data=data)
        
        if not serializers.is_valid():
            return Response(
                data   = serializers.error,
                status = status.HTTP_404_NOT_FOUND
            )
        serializers.save()
        return Response(
                data   = serializers.error,
                status = status.HTTP_201_CREATED
        )