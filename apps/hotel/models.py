from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model
from .utils import get_time
from django.urls import reverse

User = get_user_model()

class Hotel(models.Model):
    user = models.ForeignKey(
        verbose_name='manager',
        to=User,
        on_delete=models.CASCADE,
        related_name='manager'
    )
    
    REGION_CHOICES = (
        ('chuy', 'Чуйская обл.'),
        ('osh', 'Ошская обл.'),
        ('issyk-Kul', 'Иссык-Кульская обл.'),
        ('talas', 'Таласская обл.'),
        ('naryn', 'Нарынская обл.'),
        ('batken', 'Баткенская обл.'),
        ('jalal-Abad', 'Джалал-Абадская обл.')
    )
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    RAITING_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
        )

    title = models.CharField(max_length=300)
    stars = models.PositiveSmallIntegerField(choices=RAITING_CHOICES)
    slug = models.SlugField(max_length=400, primary_key=True, blank=True)
    desc = models.TextField()
    desc_list = models.CharField(max_length=300)
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    image = models.ImageField(upload_to='hotel_images')
    food = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + get_time())
        else:
            self.slug = slugify(self.title + get_time())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'
        
    def get_adsolute_url(self):
        return reverse('hotel-detail', kwargs={'pk': self.pk})



class HotelImage(models.Model):
    image = models.ImageField(upload_to='hotel_images/carousel')
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
        related_name='hotel_images'
    )

    def __str__(self) -> str:
        return f"Image to {self.hotel.title}"