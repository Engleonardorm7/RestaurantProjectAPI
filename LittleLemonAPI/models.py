from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


# class ManagersView(generics.GenericAPIView):
#     permission_classes = [IsAdminUser]

    
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         if username:
#             user = get_object_or_404(User, username=username)
#             managers = Group.objects.get(name="Manager")
#             managers.user_set.add(user)
#             return Response({"message": f"ok {user} added to the group"})
#         return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         if username:
#             user = get_object_or_404(User, username=username)
#             managers = Group.objects.get(name="Manager")
#             managers.user_set.remove(user)
#             return Response({"message": f"ok {user} removed from the group"})
#         return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)

class Category(models.Model):
    slug=models.SlugField()
    title=models.CharField(("Title"), max_length=255, db_index=True)
    
    def __str__(self):
        return self.title


class Product(models.Model):
    """
    Model class for the product.
    """
    title=models.CharField(("Title"), max_length=255)
    description=models.CharField(("Description"), max_length=255)
    price=models.DecimalField(("Price"), max_digits=8, decimal_places=2)
    image=models.ImageField(("image"), upload_to='LittleLemon/images', height_field=None, width_field=None, max_length=None)
    inventory=models.SmallIntegerField(("Inventory"))
    featured=models.BooleanField(db_index=True)
    category=models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    menuitem=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.SmallIntegerField(),
    unit_price=models.DecimalField(max_digits=6, decimal_places=2)
    price=models.DecimalField( max_digits=6, decimal_places=2)
     
    class Meta:
        unique_together=('menuitem','user')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='delivery_crew', null=True)
    status=models.BooleanField(db_index=True,default=0)
    total=models.DecimalField(max_digits=6, decimal_places=2)
    date=models.DateField(db_index=True)

class OrderItem(models.Model):
    order=models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.SmallIntegerField()
    unit_price=models.DecimalField(max_digits=6, decimal_places=2)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together=('order','menuitem')