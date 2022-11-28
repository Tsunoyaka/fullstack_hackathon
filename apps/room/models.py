from django.db import models


class Room(models.Model):
    ROOM_TYPE_CHIOCES = (
        ('standart', 'Standart'),
        ('lux', 'Lux'),
        ('vip', 'VIP')
    )
    room_title = models.CharField(max_length=300)
    room_no=models.CharField(max_length=5, primary_key=True)
    room_type=models.CharField(max_length=50, choices=ROOM_TYPE_CHIOCES)
    room_price=models.FloatField()
    room_image=models.ImageField(upload_to="media")
    
    def __str__(self):
        return self.room_no

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'




