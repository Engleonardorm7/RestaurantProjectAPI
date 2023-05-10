from rest_framework import serializers
from .models import  Category, Cart, Order, MenuItem, OrderItem #CustomUser,


from django.contrib.auth.models import User


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Esta es una subclase personalizada del serializador TokenObtainPairSerializer.
    """
    # agrega información adicional en la respuesta del token si se necesita
    user_id = serializers.IntegerField(source='user.id')
    email = serializers.EmailField(source='user.email')

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        return data



class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def to_representation(self, instance):
        # convertir el objeto User en un diccionario que se pueda serializar
        return {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email
        }

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
