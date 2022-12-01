from rest_framework import serializers
from django.db.models import Avg

from .models import Hotel, HotelImage
from apps.review.models import Comment
from apps.review.serializers import CommentSerializer, CommentImageSerializer
from apps.room.serializers import RoomSerializer

from decouple import config

class HotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('title', 'stars', 'region', 'desc_list', 'image', 'slug')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ratings = instance.comments.all()
        rating_list = []
        for r in ratings:
            if r.rating is not None:
                rating_list.append(r.rating)
                representation['avg_rating'] = round(sum(rating_list)/len(rating_list), 1)
        return representation      



class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = 'image', 

        
class HotelSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Hotel
        exclude = ('desc_list', 'user')
    
    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
            representation = super().to_representation(instance)
            ratings = instance.comments.all()
            rating_list = []
            for r in ratings:
                if r.rating is not None:
                    rating_list.append(r.rating)
                    representation['avg_rating'] = round(sum(rating_list)/len(rating_list), 1)
            representation['comments'] = CommentSerializer(
            instance.comments.all(), many=True).data
            representation['room'] = RoomSerializer(
                instance.room_manager.all(), many=True).data
            imeges = HotelImageSerializer(instance.hotel_images.all(), many=True).data
            list_ = []
            for i in imeges:
                list_.append(config('IMAGE_HOSTS') + i['image'])
            representation['hotel_images'] = list_
            return representation 


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
        hotel = Hotel.objects.create(**validated_data) 
        images = []
        for image in carousel_images:
            images.append(HotelImage(hotel=hotel, image=image))
        HotelImage.objects.bulk_create(images)
        return hotel

