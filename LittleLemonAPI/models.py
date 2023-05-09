from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# class User(models.Model):
#     email = models.EmailField(max_length=254)
#     username = models.CharField(max_length=255)
#     password = models.CharField(max_length=50)
#     # id = models.AutoField(primary_key=True)


class Category(models.Model):
    title=models.CharField(("Title"), max_length=100,unique=True, db_index=True)
    
    def __str__(self):
        return self.title


class MenuItem(models.Model):
    """
    Model class for the product.
    """
    title=models.CharField(("Title"), max_length=255)
    price=models.DecimalField(("Price"), max_digits=10, decimal_places=2)
    featured=models.BooleanField(db_index=True)
    category=models.ForeignKey(Category, on_delete=models.PROTECT)

    # description=models.CharField(("Description"), max_length=255)
    # image=models.ImageField(("image"), upload_to='LittleLemon/images', height_field=None, width_field=None, max_length=None)
    # inventory=models.SmallIntegerField(("Inventory"))


class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem=models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity=models.SmallIntegerField()
    unit_price=models.DecimalField(max_digits=10, decimal_places=2)
    price=models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together=('menuitem','user')


class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew=models.ForeignKey(User, on_delete=models.SET_NULL,related_name='delivery_crew',null=True)
    status=models.BooleanField(db_index=True,default=0)
    total=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date=models.DateField(db_index=True,auto_now_add=True)
    # created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order=models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    menuitem=models.ForeignKey(MenuItem, on_delete=models.CASCADE,default=None)
    quantity = models.IntegerField(default=1)
    unit_price=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    price=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    class Meta:
        unique_together=('order','menuitem')

