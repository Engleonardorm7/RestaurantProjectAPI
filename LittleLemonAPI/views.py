from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models import Q
from .models import MenuItem, Cart,Order,OrderItem
from .serializers import MenuItemSerializer,CartSerializer,OrderSerializer

import decimal



#-----------------------------------Product----------------

#La principal diferencia entre ListCreateAPIView y ListAPIView es que ListCreateAPIView proporciona la funcionalidad para crear nuevos objetos utilizando el método POST, además de obtener una lista de objetos utilizando el método GET, mientras que ListAPIView solo se utiliza para obtener una lista de recursos utilizando el método GET.



class MenuItems(APIView):
    """
    API View to see, edit, create or delete items.

    API endpoint: /api/menu-items/

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
        """
        Checks if the user belongs to the Manager group.

        Parameters:
        user (User): The user to check.

        Returns:
        bool: True if the user belongs to the Manager group, False otherwise.
        """
        return user.groups.filter(name='Manager').exists()
    
    def get(self, request, pk):
        """
        Retrieves a specific menu item.

        Parameters:
        request (Request): The HTTP request object.
        pk (int): The ID of the menu item to retrieve.

        Returns:
        Response: A serialized representation of the menu item.
        """
        item=get_object_or_404(MenuItem,pk=pk)
        serialized_item=MenuItemSerializer(item)
        return Response(serialized_item.data)

    def put(self, request, pk):
        """
        Updates a specific menu item.

        Parameters:
        request (Request): The HTTP request object.
        pk (int): The ID of the menu item to update.

        Returns:
        Response: A success message if the update was successful, an error message otherwise.
        """
        if self.is_manager(self.request.user):
            item=get_object_or_404(MenuItem,pk=pk)
            serialized_item=MenuItemSerializer(item,data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'mensaje':f'Product {item.title} Updated'}, status=status.HTTP_200_OK)

        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        """
        Partially updates a specific menu item.

        Parameters:
        request (Request): The HTTP request object.
        pk (int): The ID of the menu item to partially update.

        Returns:
        Response: A success message if the update was successful, an error message otherwise.
        """
        if self.is_manager(self.request.user):
            item=get_object_or_404(MenuItem,pk=pk)
            serialized_item=MenuItemSerializer(item, data=request.data, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'mensage':f'Product {item.title} Updated'}, status=status.HTTP_200_OK)

        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        """
        Deletes a specific menu item.

        Parameters:
        request (Request): The HTTP request object.
        pk (int): The ID of the menu item to delete.

        Returns:
        Response: A success message if the delete was successful, an error message otherwise.
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
        """
        Retrieve a list of all the users belonging to the 'Manager' group.

        Parameters:
        request (Request): The HTTP request object.

        Returns:
        Response: A response with a list of all the users belonging to the 'Manager' group.
        """
        if self.is_manager(self.request.user):
            managers = Group.objects.get(name='Manager') # Obtenemos el grupo Manager
            manager_users = managers.user_set.all() # Obtenemos todos los usuarios del grupo
            users_info = [{'id':user.id,'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name} for user in manager_users]
            return Response(users_info)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request):
        """
        Add a user to the 'Manager' group.

        Parameters:
        request (Request): The HTTP request object.

        Returns:
        Response: A response indicating whether the operation was successful.
        """
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
        """
        Remove a user from the 'Manager' group.

        Parameters:
        request (Request): The HTTP request object.

        Returns:
        Response: A response indicating whether the operation was successful.
        """
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
    """
    View to manage the Delivery crew user group.

    Endpoint: groups/delivery-crew/users/

    HTTP Methods:
        - GET: Get a list of all the users in the Delivery crew group.
        - POST: Add a user to the Delivery crew group.
        
    Returns:
        - GET: Returns a list with the user information for all the users in the Delivery crew group.
        - POST: Returns a message indicating that the user was added to the Delivery crew group.

    Permission:
        - IsAuthenticated: Users need to be authenticated to access this view.
    """
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
    """
    API view that handles DELETE requests to remove a user from the 'Delivery crew' group.

    Endpoint: groups/delivery-crew/users/<int:pk>/
    
    Allowed HTTP methods: DELETE
    
    Attributes:
    - permission_classes: List of permission classes that allow access to this view. Only authenticated users are allowed.
    
    Methods:
    - is_manager(self, user): Method that checks if the authenticated user is a member of the 'Manager' group.
    - delete(self, request, pk): Method that removes the user with the given pk from the 'Delivery crew' group.
    """
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
    """
    Endpoint: cart/menu-items

    Class: CartView

    This endpoint allows users to view and manage their shopping cart.

    GET:
    Returns all the items in the user's cart.
    Request: GET /cart/menu-items/
    Response:

    200 OK: Returns a list of cart items with details of each item.
    POST:
    Adds an item to the user's cart.
    Request: POST /cart/menu-items/
    Body:
    {
    "product_id": <id of menu item>,
    "quantity": <quantity of menu item>
    }
    Response:

    201 CREATED: Returns details of the item added to the cart.
    DELETE:
    Removes all the items from the user's cart.
    Request: DELETE /cart/menu-items/
    Response:

    200 OK: Returns a success message.
    Permission Classes:

    IsAuthenticated: User must be authenticated to perform any action.
    Note:

    To add an item to the cart, the user needs to provide the ID of the menu item and the quantity they want to order.
    The price of the item is calculated based on the unit price and quantity provided by the user.
    To remove a single item from the cart, the user can send a DELETE request to the URL /cart/menu-items/<id of the item>.
    """
    permission_classes = [IsAuthenticated]
   
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
    """
    Endpoint: orders

    Class: OrderView

    Description: This class-based view allows authenticated users to create, view, and delete their orders. Managers can view all orders, and delivery crew members can view and update orders assigned to them.

    Methods:

    is_manager(self, user): helper method that returns a boolean indicating whether the user is a member of the "Manager" group.
    is_delivery(self, user): helper method that returns a boolean indicating whether the user is a member of the "Delivery crew" group.
    GET:

    Description: Retrieve a list of orders. Managers can view all orders, and delivery crew members can view orders assigned to them. Regular users can only view their own orders.
    Parameters: None
    Returns: A Response object with a list of serialized Order objects.
    POST:

    Description: Create a new order based on the items in the user's cart. Deletes the cart items after the order is created.
    Parameters:
    product_id: ID of the MenuItem object to be added to the order.
    quantity: Quantity of the MenuItem to be added to the order.
    Returns: A Response object with a serialized Order object.
    DELETE:

    Description: Delete all orders created by the user.
    Parameters: None
    Returns: A Response object with a success message.
    """
    permission_classes = [IsAuthenticated]

    def is_manager(self, user):
        return user.groups.filter(name='Manager').exists()
    
    def is_delivery (self, user):
        return user.groups.filter(name='Delivery crew').exists()
        
    def get(self,request):
        
        if self.is_manager(self.request.user):
            order=Order.objects.all()
            serializer=OrderSerializer(order,many=True)
            return Response (serializer.data)
        elif self.is_delivery(self.request.user):
            order=Order.objects.filter(delivery_crew=self.request.user)
            serializer=OrderSerializer(order,many=True)
            return Response(serializer.data)
        else:
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
            # orderitemview=OrderItem.objects.create(order=order_item.order,menuitem=order_item.menuitem)
            order.save()
            order_items.append(order_item)
            total+=order_item.price
            order.total=total
            
            orderitemview=OrderItem.objects.create(
            order=order,
            menuitem=order_item.menuitem,
            quantity=order_item.quantity,
            unit_price=order_item.unit_price,
            price=order_item.price,
            )
            orderitemview.save()



        order.save()       
        CartView.delete(self,request)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self,request):
        user = request.user
        Order.objects.filter(user=user).delete()
        return Response({"message":"Items removed from the order"})

class OrderDetailView(APIView):
    
    """
    API endpoint that returns all items for an order ID. If the order ID doesn't belong to the current user, it displays an appropriate HTTP error status code.
    """
    permission_classes = [IsAuthenticated]

    def is_manager(self, user):
        """
        This method checks if the user belongs to the Manager group.

        Parameters:
        user (User): The user to be checked.

        Returns:
        bool: True if the user belongs to the Manager group, False otherwise.
        """
        return user.groups.filter(name='Manager').exists()
    
    def is_delivery (self, user):
        """
        This method checks if the user belongs to the Delivery crew group.

        Parameters:
        user (User): The user to be checked.

        Returns:
        bool: True if the user belongs to the Delivery crew group, False otherwise.
        """
        return user.groups.filter(name='Delivery crew').exists()
    
    def get(self,request,pk):
        """
        This method returns all items for an order ID.

        Parameters:
        request (Request): The HTTP request object.
        pk (int): The primary key of the order.

        Returns:
        Response: The HTTP response object.
        """
        order = get_object_or_404(Order, pk=pk)
        if order.user == request.user:
            # Obtener todos los objetos de Elemento de Pedido para el pedido actual.
            order_items = OrderItem.objects.filter(order=order)
            # Crea una lista vacía para almacenar los objetos MenuItem serializados
            menu_items = []
            # Itera a través de los objetos OrderItem y serializa los objetos MenuItem correspondientes
            for item in order_items:
                serializer = MenuItemSerializer(item.menuitem)
                menu_items.append(serializer.data)
            # Devuelve la respuesta con la lista de objetos MenuItem serializados
            return Response(menu_items, status=status.HTTP_200_OK)
        # Si el usuario actual no es el dueño del pedido, devuelve un error 404
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self,request,pk):
        """
        This method updates the status and delivery crew of an order.

        Parameters:
        request (Request): The HTTP request object.
        pk (int): The primary key of the order.

        Returns:
        Response: The HTTP response object.
        """
        order = get_object_or_404(Order, pk=pk)
        if self.is_manager(self.request.user):
            delivery_crew_id = request.data.get('delivery_crew')
            oreder_status = request.data.get('status')
            order.status = oreder_status
            if delivery_crew_id:
                delivery_crew = get_object_or_404(User, pk=delivery_crew_id)
                if self.is_delivery(delivery_crew):
                    order.delivery_crew = delivery_crew
                    order.save()
                    serializer = OrderSerializer(order)
            #return Response({'mensaje':f'{delivery_crew}\'s Order Updated'}, status=status.HTTP_200_OK)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({'mensaje':f'The user is not in the delivery crew'}, status=status.HTTP_200_OK)

        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)


    def patch(self,request,pk):
        """
        This method updates the status of an order.

        Parameters:
        request (Request): The HTTP request object.
        pk (int): The primary key of the order.

        Returns:
        Response: The HTTP response object.
        """
        order = get_object_or_404(Order, pk=pk)
        if self.is_manager(self.request.user):
            delivery_crew_id = request.data.get('delivery_crew')
            oreder_status = request.data.get('status')
            order.status = oreder_status
            if delivery_crew_id:
                delivery_crew = get_object_or_404(User, pk=delivery_crew_id)
                order.delivery_crew = delivery_crew
                order.save()
            serializer = OrderSerializer(order)
            #return Response({'mensaje':f'{delivery_crew}\'s Order Updated'}, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if self.is_delivery(self.request.user):
            oreder_status = request.data.get('status')
            order.status = oreder_status
            order.save()
            serializer = OrderSerializer(order)
            #return Response({'mensaje':f'{delivery_crew}\'s Order Updated'}, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self,request,pk):
        """
        This method deletes an order.

        Parameters:
        request (Request): The HTTP request object.
        pk (int): The primary key of the order.

        Returns:
        Response: The HTTP response object.
        """
        if self.is_manager(self.request.user):
            order=get_object_or_404(Order,pk=pk)
            if order:

                order.delete()
                return Response({'message':f'order {order.id } deleted successfully'}, status=status.HTTP_200_OK)
            return Response({'message':'The Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)


  