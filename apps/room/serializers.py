from rest_framework import serializers
from .models import Room, RoomImage, RoomNum
from decouple import config


class RoomNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomNum
        exclude = ('room_name', )

class RoomSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

    class Meta:
        model = Room
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['room_no'] = RoomNumSerializer(
            instance.room_num.all(), many=True).data
        imeges = RoomImageSerializer(instance.room_images.all(), many=True).data
        list_ = []
        for i in imeges:
            list_.append(config('IMAGE_HOSTS') + i['image'])
        representation['room_images'] = list_
        return representation


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = 'image', 


class RoomCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs
        
    carousel_img = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )

    create_room_no = serializers.ListField(
        child=serializers.CharField(max_length=500),
        write_only=True
    )

    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
        carousel_images = validated_data.pop('carousel_img')
        create_room_no = validated_data.pop('create_room_no')
        room = Room.objects.create(**validated_data)
        images = []
        room_nom = []
        for image in carousel_images:
            images.append(RoomImage(room=room, image=image))
        RoomImage.objects.bulk_create(images)
        for room_no in create_room_no:
            r = room_no.split(',')
            for p in r:
                room_nom.append(RoomNum(room_name=room, room_no=p))
        RoomNum.objects.bulk_create(room_nom)
        return room

