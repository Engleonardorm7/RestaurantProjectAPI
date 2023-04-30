from rest_framework import serializers
from .models import  Category, Cart, Order, MenuItem, OrderItem #CustomUser,

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=CustomUser
        
#         fields = ['id', 'username', 'email','password']#, 'is_delivery_crew', 'is_manager'
#         extra_kwargs = {'password': {'write_only': True}}

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    class Meta:
        model=MenuItem
        fields=['id','title','price','featured','category']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(source='menuitem')
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']

# class OrderItemSerializer(serializers.ModelSerializer):
#     product=ProductSerializer()

#     class Meta:
#         model=OrderItem
#         fields=['id','product','quantity','price']

# class OrderSerializer(serializers.ModelSerializer):
#     items=OrderItemSerializer(many=True)

#     class Meta:
#         model=Order
#         fields = ['id', 'user', 'created_at', 'updated_at', 'is_ordered', 'total_price', 'items']

# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')