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
from .models import Product, Category
from .serializers import ProductSerializer,CategorySerializer

from django.contrib.auth.decorators import user_passes_test


# class CustomUserListCreateView(generics.ListCreateAPIView):
#     """
#     API View to create a user.
#     """
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data.get('username')
#             email = serializer.validated_data.get('email')
#             if not CustomUser.objects.filter(Q(username=username) | Q(email=email)).exists():
#                 serializer.save()
#                 return Response({'message': f'User {username} created successfully.'}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({'error': 'User with that username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class UserDetailsView(APIView):
#     """
#     API view to see the current user or the list of users
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         serializer = CustomUserSerializer(request.user)
#         return Response(serializer.data)

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
        menu_items = Product.objects.all()
        serializer = ProductSerializer(menu_items, many=True)
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
            serialized_item=ProductSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'mensaje': f'Product {ProductSerializer.fields__title} Created'},status=status.HTTP_201_CREATED)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        if self.is_manager(self.request.user):
            item=self.get_object(pk)
            serialized_item=ProductSerializer(item,data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'mensaje':f'Product {item.title} Updated'}, status=status.HTTP_200_OK)

        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        if self.is_manager(self.request.user):
            item=self.get_object(pk)
            serialized_item=ProductSerializer(item, data=request.data, partial=True)
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
        item=get_object_or_404(Product,pk=pk)
        serialized_item=ProductSerializer(item)
        return Response(serialized_item.data)

    def put(self, request, pk):
        """Update a specific item with the provided data."""
        if self.is_manager(self.request.user):
            item=get_object_or_404(Product,pk=pk)
            serialized_item=ProductSerializer(item,data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'mensaje':f'Product {item.title} Updated'}, status=status.HTTP_200_OK)

        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        """Partially update a specific item with the provided data."""
        if self.is_manager(self.request.user):
            item=get_object_or_404(Product,pk=pk)
            serialized_item=ProductSerializer(item, data=request.data, partial=True)
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
            item=get_object_or_404(Product,pk=pk)
            item.delete()
            return Response({'mensaje': f'Product {item.title} Updated'}, status=status.HTTP_200_OK)
        return Response({'mensaje': 'Access Denied'},status=status.HTTP_403_FORBIDDEN)


class Managers(APIView):
    
    def is_manager(self, user):
        return user.groups.filter(name='Manager').exists()
    
    def get(self, request):
        managers = Group.objects.get(name='Manager') # Obtenemos el grupo Manager
        manager_users = managers.user_set.all() # Obtenemos todos los usuarios del grupo
        # Creamos una lista de diccionarios con información de cada usuario para serializar en la respuesta
        users_info = [{'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name} for user in manager_users]
        return Response(users_info)


















class ManagersView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        username = request.data.get('username', None)
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.add(user)
            return Response({"message":f"ok {user} added to the group"})
        return Response({'message':'error'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        username = request.data.get('username', None)
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.remove(user)
            return Response({"message":f"ok {user} removed from the group"})
        return Response({'message':'error'}, status=status.HTTP_400_BAD_REQUEST)