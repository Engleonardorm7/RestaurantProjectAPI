from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.response import Response



class CustomUser(AbstractUser):
    """
    Model class for Custom User.
    """
    username=models.CharField(("Username"), max_length=200, unique=True)
    email=models.EmailField(("Email"), max_length=254, unique=True)
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['username','email']
    # is_delivery_crew=models.BooleanField(("Delivery crew"),default=False)
    # is_manager=models.BooleanField(("Manager"),default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=('The groups this user belongs to. A user will '
                   'get all permissions granted to each of '
                   'their groups.'),
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='customuser_set',
        related_query_name='user'
    )

class ManagersView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.add(user)
            return Response({"message": f"ok {user} added to the group"})
        return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.remove(user)
            return Response({"message": f"ok {user} removed from the group"})
        return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)

class Category(models.Model):
    title=models.CharField(("Title"), max_length=100,unique=True)
    
    def __str__(self):
        return self.title


class Product(models.Model):
    """
    Model class for the product.
    """
    title=models.CharField(("Title"), max_length=255)
    description=models.CharField(("Description"), max_length=255)
    price=models.DecimalField(("Price"), max_digits=6, decimal_places=2)
    image=models.ImageField(("image"), upload_to='LittleLemon/images', height_field=None, width_field=None, max_length=None)
    inventory=models.SmallIntegerField(("Inventory"))
    category=models.ForeignKey(Category, on_delete=models.PROTECT, default=1)


class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)