from django.db import models
from apps.hotel.models import Hotel
from slugify import slugify

from .utils import get_time



class Room(models.Model):
    ROOM_TYPE_CHIOCES = (
        ('standart', 'Standart'),
        ('lux', 'Lux'),
        ('vip', 'VIP')
    )
    ROOM_CAPACITY_CHIOCES = (
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('quadruple', 'Quadruple')
    )
    room_title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200, db_index=True, blank=True, primary_key=True)
    room_type=models.CharField(max_length=50, choices=ROOM_TYPE_CHIOCES)
    room_capacity = models.CharField(max_length=50, choices=ROOM_CAPACITY_CHIOCES)
    room_price=models.DecimalField(max_digits=10, decimal_places=2)
    room_image=models.ImageField(upload_to="media")
    # дополнительные данные:
    room_area = models.PositiveIntegerField()
    balcony = models.BooleanField(default=False)
    garden_view = models.BooleanField(default=False)
    mountain_view = models.BooleanField(default=False)
    landmark_view = models.BooleanField(default=False)
    city_view = models.BooleanField(default=False)
    air_conditioner = models.BooleanField(default=False)
    private_bathroom = models.BooleanField(default=False)
    flat_screen_TV = models.BooleanField(default=False)
    soundproofing = models.BooleanField(default=False)
    sauna = models.BooleanField(default=False)
    mini_bar = models.BooleanField(default=False)
    free_wifi = models.BooleanField(default=False)
    coffee_machine = models.BooleanField(default=False)
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
        related_name='hotels'
    )
    
    def __str__(self):
        return self.room_title

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.room_title + get_time())
        super().save(*args, **kwargs)


class RoomImage(models.Model):
    image = models.ImageField(upload_to='media')
    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
        related_name='images'
    )

    def __str__(self) -> str:
        return f"Image to {self.room.title}"


class RoomNum(models.Model):
    room_no = models.CharField(max_length=10)
    room_name = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
        related_name='comment_images'
    )
    is_booked = models.BooleanField(default=False)
    


# TODO добавить дополнительные услуги комнаты
# T ODO 





