from django.db import models
from apps.hotel.models import Hotel
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    RAITING_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5'),
        (SIX, '6'),
        (SEVEN, '7'),
        (EIGHT, '8'),
        (NINE, '9'),
        (TEN, '10'),
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    rating = models.FloatField(blank=True, null=True)
    good_review = models.TextField(blank=True, null=True)
    bad_review = models.TextField(blank=True, null=True)
    staff = models.PositiveSmallIntegerField(choices=RAITING_CHOICES, blank=True, null=True)
    comfort = models.PositiveSmallIntegerField(choices=RAITING_CHOICES, blank=True, null=True)
    purity = models.PositiveSmallIntegerField(choices=RAITING_CHOICES, blank=True, null=True)
    price_quality_ratio = models.PositiveSmallIntegerField(choices=RAITING_CHOICES, blank=True, null=True)
    location = models.PositiveSmallIntegerField(choices=RAITING_CHOICES, blank=True, null=True)
    facilities = models.PositiveSmallIntegerField(choices=RAITING_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        number_list = [self.staff, self.comfort, self.purity, self.price_quality_ratio, self.location, self.facilities]
        self.rating = sum(number_list)/len(number_list)
        super().save(*args, **kwargs)

    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return f'Comment from {self.user.username} to {self.hotel.title}'


class CommentImage(models.Model):
    image = models.ImageField(upload_to='comment_images/carousel')
    comment = models.ForeignKey(
        to=Comment,
        on_delete=models.CASCADE,
        related_name='comment_images'
    )

    def str(self) -> str:
        return f'Image to {self.comment.hotel}'
