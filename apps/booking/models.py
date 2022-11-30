from django.db import models
from datetime import timedelta, datetime

from apps.account.models import User
from apps.hotel.models import Hotel
from apps.room.models import Room


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    num_of_guest = models.IntegerField(default=1)
    checkin_date = models.DateField(default=datetime.now)
    checkout_date = models.DateField(default=datetime.now)
    is_checkout = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

    def hotel_name(self) -> str:
        return self.hotel.hotel

    def charge(self) -> float:
        return self.is_checkout* \
        (self.checkout_date - self.checkin_date + timedelta(1)).days* \
        self.room.price