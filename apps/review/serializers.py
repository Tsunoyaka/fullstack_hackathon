from rest_framework import serializers
from .models import Comment, CommentImage
from django.db.models import Avg


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(default=serializers.CurrentUserDefault(), source='user.username')

    class Meta:
        model = Comment
        exclude = ('id', 'hotel')

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comment_images'] = CommentImageSerializer(
        instance.comment_images.all(), many=True).data
        return representation


class CommentRatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )
    
    # class Meta:
    #     model = Comment
    #     fields = ('rating', 'user', 'hotel')
        
    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating')
        if rating not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
            raise serializers.ValidationError('Wrong value! Rating must be between from 1 to 10'
            )
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        return super().update(instance, validated_data)


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = 'image', 


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )
    carousel_img = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        carousel_images = validated_data.pop('carousel_img')
        comment = Comment.objects.create(**validated_data)
        images = []
        for image in carousel_images:
            images.append(CommentImage(comment=comment, image=image))
        CommentImage.objects.bulk_create(images)
        return comment