from rest_framework import serializers
from .models import  Category, OrderItem, Order, Product #CustomUser,

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

class OrderItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer()

    class Meta:
        model=OrderItem
        fields=['id','product','quantity','price']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)

    class Meta:
        model=Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'is_ordered', 'total_price', 'items']
