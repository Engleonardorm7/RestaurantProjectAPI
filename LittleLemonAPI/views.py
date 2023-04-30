from rest_framework import generics, status
# from .models import CustomUser
# from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated,BasePermission
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models import Q
<<<<<<< HEAD
from .models import Product, Cart
from .serializers import ProductSerializer,CartSerializer,OrderSerializer,OrderItemSerializer
=======
from .models import MenuItem, Cart,Order,OrderItem
from .serializers import MenuItemSerializer,CartSerializer,OrderSerializer,OrderItemSerializer
>>>>>>> 9dca2ad

import decimal

#-----------------------------------Product----------------

#La principal diferencia entre ListCreateAPIView y ListAPIView es que ListCreateAPIView proporciona la funcionalidad para crear nuevos objetos utilizando el método POST, además de obtener una lista de objetos utilizando el método GET, mientras que ListAPIView solo se utiliza para obtener una lista de recursos utilizando el método GET.



class MenuItems(APIView):
    """
    API View to see, edit, create or delete items.

    GET:
    Returns a list of all menu items.

    POST:
    Creates a new menu item.

    PUT:
    Updates an existing menu item.

    PATCH:
    Partially updates an existing menu item.

    DELETE:
    Deletes an existing menu item.
    """
    permission_classes = [IsAuthenticated]
    
    def is_manager(self, user):
        """
        Check if the user is a Manager.

        Parameters:
        user (User): The user instance to check.

        Returns:
        bool: True if the user is a Manager, False otherwise.
        """
        return user.groups.filter(name='Manager').exists()
    
    def get(self, request):
        """
        Returns a list of all menu items.

        Returns:
        Response: A response with serialized menu items.
        """
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a new menu item.

        Parameters:
        request (Request): The HTTP request object.

        Returns:
        Response: A response with the created menu item data.
        """
        if self.is_manager(self.request.user):
            serialized_item=MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'mensaje': f'Product {MenuItemSerializer.fields__title} Created'},status=status.HTTP_201_CREATED)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        if self.is_manager(self.request.user):
            item=self.get_object(pk)
            serialized_item=MenuItemSerializer(item,data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'mensaje':f'Product {item.title} Updated'}, status=status.HTTP_200_OK)

        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        if self.is_manager(self.request.user):
            item=self.get_object(pk)
            serialized_item=MenuItemSerializer(item, data=request.data, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'mensage':f'Product {item.title} Updated'}, status=status.HTTP_200_OK)

        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        if self.is_manager(self.request.user):
            item=self.get_object(pk)
            item.delete()
            return Response({'mensaje': f'Product {item.title} Updated'}, status=status.HTTP_200_OK)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)

    # def get_object(self, request, pk):
    #     try:
    #         return Product.objects.get(pk=pk)
    #     except Product.DoesNotExist:
    #         raise status.HTTP_404_NOT_FOUND
        
class MenuItemDetailView(APIView):

    """
    API View to view, edit, create or delete a specific item.

    GET:
    Return a serialized representation of a specific item.

    PUT:
    Update a specific item with the provided data.

    PATCH:
    Partially update a specific item with the provided data.

    DELETE:
    Delete a specific item.

    Permission Classes:
    - IsAuthenticated: Allow access only to authenticated users.
    - IsManager: Allow access only to users belonging to the 'Manager' group.
    """
    permission_classes = [IsAuthenticated]

    def is_manager(self, user):
        return user.groups.filter(name='Manager').exists()
    
    def get(self, request, pk):
        item=get_object_or_404(MenuItem,pk=pk)
        serialized_item=MenuItemSerializer(item)
        return Response(serialized_item.data)

    def put(self, request, pk):
        """Update a specific item with the provided data."""
        if self.is_manager(self.request.user):
            item=get_object_or_404(MenuItem,pk=pk)
            serialized_item=MenuItemSerializer(item,data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'mensaje':f'Product {item.title} Updated'}, status=status.HTTP_200_OK)

        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        """Partially update a specific item with the provided data."""
        if self.is_manager(self.request.user):
            item=get_object_or_404(MenuItem,pk=pk)
            serialized_item=MenuItemSerializer(item, data=request.data, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'mensage':f'Product {item.title} Updated'}, status=status.HTTP_200_OK)

        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        """
        Deletes an existing menu item.

        Parameters:
        request (Request): The HTTP request object.
        pk (int): The ID of the menu item to delete.

        Returns:
        Response: A response with a success message.
        """
        if self.is_manager(self.request.user):
            item=get_object_or_404(MenuItem,pk=pk)
            item.delete()
            return Response({'mensaje': f'Product {item.title} Updated'}, status=status.HTTP_200_OK)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)


class Managers(APIView):

    permission_classes = [IsAuthenticated]

    def is_manager(self, user):
        return user.groups.filter(name='Manager').exists()
    
    def get(self, request):
        if self.is_manager(self.request.user):
            managers = Group.objects.get(name='Manager') # Obtenemos el grupo Manager
            manager_users = managers.user_set.all() # Obtenemos todos los usuarios del grupo
            users_info = [{'id':user.id,'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name} for user in manager_users]
            return Response(users_info)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request):
        if self.is_manager(self.request.user):
            username = request.data.get('username', None)
            if username:
                user = get_object_or_404(User, username=username)
                managers = Group.objects.get(name="Manager")
                managers.user_set.add(user)
                return Response({"message":f"ok {user} added to the group"}, status=status.HTTP_201_CREATED)
            return Response({'message':'The user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)


#Delete by username
    def delete(self,request):
        if self.is_manager(self.request.user):
            username=request.data.get('username', None)
            if username:
                user=get_object_or_404(User,username=username)
                managers=Group.objects.get(name="Manager")
                managers.user_set.remove(user)
                return Response({"message":f"ok {user} deleted from the group"})
            return Response({'message':'The user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)



# #delete by ID
# class ManagerSingleView(APIView):

#     permission_classes = [IsAuthenticated]

#     def is_manager(self, user):
#         return user.groups.filter(name='Manager').exists()
    
#     def get(self, request, id):
#         if self.is_manager(self.request.user):
#             manager=get_object_or_404(User, id=id)
#         return Response(manager.data)


class DeliveryCrewView(APIView):
    permission_classes = [IsAuthenticated]

    def is_manager(self,user):
        return user.groups.filter(name="Manager").exists()
    
    def get(self,request):
        if self.is_manager(self.request.user):
            delivery=Group.objects.get(name="Delivery crew")
            delivery_crew=delivery.user_set.all()
            delivery_crew_info=[{'id':user.id,'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name} for user in delivery_crew]  
            return Response(delivery_crew_info)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)
    
    def post(self,request):
        if self.is_manager(self.request.user):
            username=request.data.get("username",None)
            if username:
                user=get_object_or_404(User,username=username)
                delivery_crew=Group.objects.get(name='Delivery crew')
                delivery_crew.user_set.add(user)
                return Response({"message":f"ok {user} added to the Delivery group"}, status=status.HTTP_201_CREATED)
            return Response({'message':'The user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)


class DeleteDeliveryCrewView(APIView):
    permission_classes = [IsAuthenticated]

    def is_manager(self,user):
        return user.groups.filter(name="Manager").exists()
    
    def delete(self,request,pk):
        if self.is_manager(self.request.user):
            user=get_object_or_404(User,pk=pk)
            if user:
                delivery_crew=Group.objects.get(name='Delivery crew')
                delivery_crew.user_set.remove(user)
                return Response({"message":f"ok {user} deleted from the Delivery group"})
            return Response({'message':'The user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)



class CartView(APIView):
    permission_classes = [IsAuthenticated]
<<<<<<< HEAD
    """
        API endpoint that allows customers to get, add or delete menu items from their cart.
    """
    serializer_class = CartSerializer
    def get(self, request):
        user=request.user
        cart_items=Cart.objects.filter(user=user)
        serializer=self.serializer_class(cart_items,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        pass

    def delete(self, request):
        pass


# def post(self, request, *args, **kwargs):
#         user = request.user
#         menuitem_id = request.data.get('menuitem_id')
#         quantity = request.data.get('quantity')

#         # Create cart item
#         try:
#             cart_item = Cart.objects.create(user=user, menuitem_id=menuitem_id, quantity=quantity)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = self.serializer_class(cart_item)
#         return Response(serializer.data)

#     def delete(self, request, *args, **kwargs):
#         user = request.user
#         Cart.objects.filter(user=user).delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
=======
   
    def get(self,request):
        carts=Cart.objects.filter(user=self.request.user)
        serializer=CartSerializer(carts,many=True)
        return Response (serializer.data)

    def post(self,request):
        user = request.user
        menuitem_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        menuitem = get_object_or_404(MenuItem, id=menuitem_id)
        unit_price = menuitem.price
        price = unit_price * decimal.Decimal(quantity)
        cart_item = Cart.objects.create(
            user=user,
            menuitem=menuitem,
            quantity=quantity,
            unit_price=unit_price,
            price=price
        )
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=201)

    def delete(self,request):
        user = request.user
        Cart.objects.filter(user=user).delete()
        return Response({"message":"Items removed from cart"})


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        order=Order.objects.filter(user=self.request.user)
        serializer=OrderSerializer(order,many=True)
        return Response (serializer.data)
    
    def post(self,request):
        cart_items = Cart.objects.filter(user=request.user)
        order = Order.objects.create(user=request.user)
        order_items=[]
        total=0
        for cart_item in cart_items:
            order_item=OrderItem(
                order=order,
                
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
                )
            order.save()
            order_items.append(order_item)
            total+=order_item.price
        order.total=total
        order.save()
        
        CartView.delete(self,request)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        
        order = get_object_or_404(Order, id=pk)
        if order.user==request.user:
            items = order.items.all()
            order_item=OrderItem(
                order=order.user,
                
                menuitem=items.menuitem,
                quantity=items.quantity,
                unit_price=order_item.unit_price,
                price=order_item.price
                )

            serializer = OrderSerializer(order_item, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
        
>>>>>>> 9dca2ad
