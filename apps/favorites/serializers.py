from requests import Response
from rest_framework import serializers

from .models import Favorites



class FavoritesSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = Favorites
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        hotel = self.context.get('request').data.get('hotel')
        favorite = Favorites.objects.filter(user=user, hotel=hotel).first()
        if favorite:
            favorite.delete()
            raise serializers.ValidationError('Unfavorite')
        return super().create(validated_data)
    




