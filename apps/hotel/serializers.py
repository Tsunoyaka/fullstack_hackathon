from rest_framework import serializers
from django.db.models import Avg

from .models import Hotel, HotelImage
from apps.review.models import Comment
from apps.review.serializers import CommentSerializer, CommentImageSerializer
from django_filters import rest_framework as rest_filter


class HotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('title', 'stars', 'desc_list')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(
        instance.comments.all(), many=True
        ).data
        representation['hotel_image'] = HotelImageSerializer(
            instance.hotel_images.all(), many=True).data
        return representation      


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = 'image', 

        
class HotelSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Hotel
        fields = '__all__'
    
    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class HotelCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )
    carousel_img = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )

    class Meta:
        model = Hotel
        fields = '__all__'

    def create(self, validated_data):
        carousel_images = validated_data.pop('carousel_img')
        # region = validated_data.pop('region')
        hotel = Hotel.objects.create(**validated_data)
        # hotel.region.set(region)
        images = []
        for image in carousel_images:
            images.append(HotelImage(hotel=hotel, image=image))
        HotelImage.objects.bulk_create(images)
        return hotel