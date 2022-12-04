from django.db import models
from apps.hotel.models import Hotel
from django.contrib.auth import get_user_model


User = get_user_model()

class Favorites(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='favorit'
    )
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
        related_name='favorit'
    )

    def __str__(self) -> str:
        return f'Hotel {self.hotel.title}'

