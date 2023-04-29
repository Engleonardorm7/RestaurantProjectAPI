from rest_framework import serializers
from .models import  Category, OrderItem, Order, Product, User, Cart #CustomUser,

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=CustomUser
        
#         fields = ['id', 'username', 'email','password']#, 'is_delivery_crew', 'is_manager'
#         extra_kwargs = {'password': {'write_only': True}}

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title']

class ProductSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    class Meta:
        model=Product
        fields=['id','title','description','price','image','inventory','category']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem','quantity', 'unit_price', 'price']



class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
