from rest_framework import serializers
from django.db.models import Avg

from .models import Hotel, HotelImage
from apps.review.models import Comment
from apps.review.serializers import CommentSerializer, CommentImageSerializer


class HotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('title', 'stars', 'region', 'desc_list', 'image')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ratings = instance.comments.all()
        rating_list = []
        for r in ratings:
            if r.rating is not None:
                rating_list.append(r.rating)
                representation['avg_rating'] = round(sum(rating_list)/len(rating_list), 1)
        # representation['comments'] = CommentSerializer(
        # instance.comments.all(), many=True
        # ).data
        # representation['hotel_image'] = HotelImageSerializer(
        #     instance.hotel_images.all(), many=True).data
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

    def to_representation(self, instance):
            representation = super().to_representation(instance)
            ratings = instance.comments.all()
            rating_list = []
            for r in ratings:
                if r.rating is not None:
                    rating_list.append(r.rating)
                    representation['avg_rating'] = round(sum(rating_list)/len(rating_list), 1)
            representation['comments'] = CommentSerializer(
            instance.comments.all(), many=True
            ).data
            representation['hotel_image'] = HotelImageSerializer(
                instance.hotel_images.all(), many=True).data
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
        region = validated_data.pop('region')
        hotel = Hotel.objects.create(**validated_data)
        hotel.region.set(region)
        images = []
        for image in carousel_images:
            images.append(HotelImage(hotel=hotel, image=image))
        HotelImage.objects.bulk_create(images)
        return hotel


