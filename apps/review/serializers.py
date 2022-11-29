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

    # def create(self, validated_data):
    #     carousel_images = validated_data.pop('carousel_img')
    #     comment = Comment.objects.create(**validated_data)
    #     images = []
    #     for image in carousel_images:
    #         images.append(CommentImage(comment=comment, image=image))
    #     CommentImage.objects.bulk_create(images)
    #     return comment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comment_images'] = CommentImageSerializer(
        instance.comment_images.all(), many=True).data
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
        fields = '__all__'

    def create(self, validated_data):
        carousel_images = validated_data.pop('carousel_img')
        comment = Comment.objects.create(**validated_data)
        images = []
        for image in carousel_images:
            images.append(CommentImage(comment=comment, image=image))
        CommentImage.objects.bulk_create(images)
        return comment
