from django.db import models
from apps.hotel.models import Hotel
from slugify import slugify
from django.contrib.auth import get_user_model
from .utils import get_time

User = get_user_model()


class Room(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='room_manager'
    )
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
        related_name='room_manager'
    )
    

    ROOM_TYPE_CHIOCES = (
        ('standart', 'Standart'),
        ('lux', 'Lux'),
        ('vip', 'VIP')
    )
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

    ROOM_CAPACITY_CHIOCES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4')
    )
    slug = models.SlugField(max_length=200, db_index=True, blank=True, primary_key=True)
    room_type=models.CharField(max_length=50, choices=ROOM_TYPE_CHIOCES)
    room_capacity = models.PositiveSmallIntegerField(choices=ROOM_CAPACITY_CHIOCES)
    room_price=models.DecimalField(max_digits=10, decimal_places=2)
    # дополнительные данные:
    air_conditioner = models.BooleanField(default=False)
    flat_screen_TV = models.BooleanField(default=False)
    free_wifi = models.BooleanField(default=False)

    def __str__(self):
        return self.room_type

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def save(self, *args, **kwargs):
        if self.room_type == 'standart':
            self.flat_screen_TV = True
        if self.room_type == 'lux':
            self.flat_screen_TV = True
            self.free_wifi = True
        if self. room_type == 'vip':
            self.flat_screen_TV = True
            self.free_wifi = True
            self.air_conditioner = True            
        if not self.slug:
            self.slug = slugify(self.room_type + get_time())
        super().save(*args, **kwargs)


class RoomImage(models.Model):
    image = models.ImageField(upload_to='room_images')
    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
        related_name='room_images'
    )

    def __str__(self) -> str:
        return f"Image to {self.room.room_type}"


class RoomNum(models.Model):
    room_no = models.CharField(max_length=10)
    room_name = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
        related_name='room_num'
    )
    is_booked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Image to {self.room_name.room_type}"

