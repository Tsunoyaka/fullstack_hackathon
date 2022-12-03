# Generated by Django 4.1.3 on 2022-12-02 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('title', models.CharField(max_length=300)),
                ('stars', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('slug', models.SlugField(blank=True, max_length=400, primary_key=True, serialize=False)),
                ('desc', models.TextField()),
                ('desc_list', models.CharField(max_length=300)),
                ('region', models.CharField(choices=[('chuy', 'Чуйская обл.'), ('osh', 'Ошская обл.'), ('issyk-Kul', 'Иссык-Кульская обл.'), ('talas', 'Таласская обл.'), ('naryn', 'Нарынская обл.'), ('batken', 'Баткенская обл.'), ('jalal-Abad', 'Джалал-Абадская обл.')], max_length=50)),
                ('adress', models.CharField(max_length=300)),
                ('image', models.ImageField(upload_to='hotel_images')),
                ('food', models.BooleanField(default=False)),
                ('pets', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Отель',
                'verbose_name_plural': 'Отели',
            },
        ),
        migrations.CreateModel(
            name='HotelImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='hotel_images/carousel')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_images', to='hotel.hotel')),
            ],
        ),
    ]
