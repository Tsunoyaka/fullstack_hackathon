from rest_framework import serializers

from apps.hotel.models import Hotel
from .models import Comment, Dislike, Like
from django.db.models import Avg


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(default=serializers.CurrentUserDefault(), source='user.username')

    class Meta:
        model = Comment
        fields = ('id','user','rating', 'good_review', 'bad_review', 'created_at')

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.likes.all().count()
        representation['dislike'] = instance.dislikes.all().count()
        return representation


class CommentCRUDSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = Comment
        fields = '__all__'


    def create(self, validated_data):
        user = self.context.get('request').user
        hotel = self.context.get('request').data.get('hotel')
        comment_ = Comment.objects.filter(user=user, hotel=hotel).first()
        if comment_:
            raise serializers.ValidationError('Вы уже комментировали!')
        comment = Comment.objects.create(**validated_data)
        return comment


class CommentDelUpdSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )
    class Meta:
        model = Comment
        fields = '__all__'


    def delete(self):
        user = self.context.get('request').user
        comment = Comment.objects.filter(user=user).first()
        if comment:
            comment.delete()
        else:
            raise serializers.ValidationError('Вы еще не комментировали!')

    def update(self, instance: Comment, validated_data):
        instance.good_review = validated_data.get('good_review', instance.good_review) 
        instance.bad_review = validated_data.get('bad_review', instance.bad_review)
        instance.staff = validated_data.get('staff', instance.staff)
        instance.comfort = validated_data.get('comfort', instance.comfort)
        instance.purity = validated_data.get('purity', instance.purity)
        instance.location = validated_data.get('location', instance.location)
        instance.facilities = validated_data.get('facilities', instance.facilities) 
        instance.price_quality_ratio = validated_data.get('price_quality_ratio', instance.price_quality_ratio)

        instance.save()
        return instance
       


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        comment = self.context.get('request').data.get('comment')
        user = self.context.get('request').user
        dislike = Dislike.objects.filter(user=user, comment=comment).first()
        if dislike:
            dislike.delete()
        like = Like.objects.filter(user=user, comment=comment).first()
        if like:
            raise serializers.ValidationError('Already liked')
        return super().create(validated_data)

    def unlike(self):
        comment = self.context.get('request').data.get('comment')
        user = self.context.get('request').user
        like = Like.objects.filter(user=user, comment=comment).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('Not liked yet')


class DislikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = Dislike
        fields = '__all__'

    def create(self, validated_data):
        comment = self.context.get('request').data.get('comment')
        user = self.context.get('request').user
        like = Like.objects.filter(user=user, comment=comment).first()
        if like:
            like.delete()
        dislike = Dislike.objects.filter(user=user, comment=comment).first()
        if dislike:
            raise serializers.ValidationError('Already disliked')
        return super().create(validated_data)

    def undislike(self):
        comment = self.context.get('request').data.get('comment')
        user = self.context.get('request').user
        dislike = Like.objects.filter(user=user, comment=comment).first()
        if dislike:
            dislike.delete()
        else:
            raise serializers.ValidationError('Not disliked yet')

