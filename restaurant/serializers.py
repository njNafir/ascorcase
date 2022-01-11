from rest_framework import serializers
from .models import *


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('owner', 0):
            if not attrs.get('owner').restaurant_owner:
                raise serializers.ValidationError("User not a restaurant owner")
        elif attrs.get('owner', 0) == 0:
            raise serializers.ValidationError("Owner required!")
        return attrs


class MenuSerializer(serializers.ModelSerializer):
    items = serializers.CharField(max_length=255)

    class Meta:
        model = Menu
        fields = [
            'restaurant',
            'title', 
            'description', 
            'price', 
            'is_active', 
            'items',
            'menu_active_date'
        ]


class MenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['restaurant', 'title', 'description', 'price']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
