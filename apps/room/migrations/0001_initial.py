# Generated by Django 4.1.3 on 2022-11-29 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_title', models.CharField(max_length=300)),
                ('room_no', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('room_type', models.CharField(choices=[('standart', 'Standart'), ('lux', 'Lux'), ('vip', 'VIP')], max_length=50)),
                ('room_price', models.FloatField()),
                ('room_image', models.ImageField(upload_to='media')),
            ],
            options={
                'verbose_name': 'Комната',
                'verbose_name_plural': 'Комнаты',
            },
        ),
    ]
