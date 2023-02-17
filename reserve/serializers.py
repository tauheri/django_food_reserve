from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import Food, Menu, MenuReservation, User
# from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'title', 'description', 'price', 'discount', 'image_url', 'discounted_price']

    discounted_price = serializers.SerializerMethodField(method_name='calculate_discount_price')
    image_url = serializers.SerializerMethodField(method_name='get_image_url')

    def calculate_discount_price(self, food: Food):
        if food.discount is not None:
            return food.price * (100.0 - float(food.discount)) * 0.01
        else:
            return None

    def get_image_url(self, food):
        request = self.context.get('request')
        if food.image:
            image_url = food.image.url
            return request.build_absolute_uri(image_url)
        else:
            return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'telegram_id']


class MenuReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # menu = serializers.StringRelatedField()
    food = FoodSerializer()
    class Meta:
        model = MenuReservation
        fields = ['id', 'user', 'food', 'quantity', 'placed_at']


class MenuSerializer(serializers.ModelSerializer):
    foods = FoodSerializer(source='get_foods', many=True)
    reservations = MenuReservationSerializer(many=True)
    class Meta:
        model = Menu
        fields = ['id', 'date', 'foods', 'isActive', 'reservations']
        

class NormalUsersMenuSerializer(serializers.ModelSerializer):
    foods = FoodSerializer(source='get_foods', many=True)
    reservations = MenuReservationSerializer(source='filtered_reservations', many=True)
    class Meta:
        model = Menu
        fields = ['id', 'date', 'foods', 'isActive', 'reservations']


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attr):
        data = super().validate(attr)
        data['is_superuser'] = self.user.is_superuser
        return data


# #This needs token decoding to get the custom fields
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['is_superuser'] = user.is_superuser
#         return token