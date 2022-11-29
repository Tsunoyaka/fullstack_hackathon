from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model
from .utils import get_time


User = get_user_model()

class Region(models.Model):
    REGION_CHOICES = (
        ('chuy', 'Чуй'),
        ('osh', 'Ош'),
        ('issyk-Kul', 'Иссык-Куль'),
        ('talas', 'Талас'),
        ('naryn', 'Нарын'),
        ('batken', 'Баткен'),
        ('jalal-Abad', 'Джалал-Абад')
    )
    region = models.CharField(max_length=100, choices=REGION_CHOICES, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True, blank=True)
    def __str__(self) -> str:
        return self.region

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.region)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'


class Hotel(models.Model):
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
    region = models.ForeignKey(Region, related_name='regions', on_delete=models.CASCADE)
    adress = ...
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


class HotelImage(models.Model):
    image = models.ImageField(upload_to='hotel_images/carousel')
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
        related_name='hotel_images'
    )

    def __str__(self) -> str:
        return f"Image to {self.hotel.title}"

  