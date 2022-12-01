from rest_framework import serializers
from .models import Comment, CommentImage
from django.db.models import Avg
from decouple import config

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(default=serializers.CurrentUserDefault(), source='user.username')

    class Meta:
        model = Comment
        fields = ('user','rating', 'good_review', 'bad_review', 'created_at', 'comment_images')

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        imeges = CommentImageSerializer(instance.comment_images.all(), many=True).data
        list_ = []
        for i in imeges:
            list_.append(config('IMAGE_HOSTS') + i['image'])
        representation['comment_images'] = list_
        return representation




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
        exclude = ('hotel',)

    def create(self, validated_data):
        carousel_images = validated_data.pop('carousel_img')
        comment = Comment.objects.create(**validated_data)
        images = []
        for image in carousel_images:
            images.append(CommentImage(comment=comment, image=image))
        CommentImage.objects.bulk_create(images)
        return comment
