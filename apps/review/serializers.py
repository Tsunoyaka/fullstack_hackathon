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


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = 'image', 


class CommentCRUDSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )
    # carousel_img = serializers.ListField(
    #     child=serializers.FileField(),
    #     write_only=True
    # )

    class Meta:
        model = Comment
        fields = '__all__'

    # def validate(self, attrs):
    #     # user = self.context['request'].user
    #     attrs['user'] = user
    #     return attrs

    def create(self, validated_data):
        
        # carousel_images = validated_data.pop('carousel_img')
        # comment = Comment.objects.create(**validated_data)
        # images = []
        # for image in carousel_images:
        #     images.append(CommentImage(comment=comment, image=image))
        # CommentImage.objects.bulk_create(images)
        # return comment
        return super().create(validated_data)

    def update(self, instance: Comment, validated_data):
        # return super().update(instance, validated_data)
        instance.staff = validated_data.staff if validated_data.staff else instance.staff

        instance.save()

    # def delete(self):
    #     user = self.context.get('request').user
    #     comment = self.context.get('comment')
    #     comment = Comment.objects.filter(user=user, comment=comment).first()
    #     if comment:
    #         comment.delete()
    #     else:
    #         raise serializers.ValidationError('Вы еще не комментировали!')

    # def update(self):
    #     user = self.context.get('request').user
    #     comment = self.context.get('comment')