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
from .serializers import ProductSerializer

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
#     API View to see, edit, create or delete items.
#     """
    permission_classes = [IsAuthenticated]
    
    def is_manager(self, user):
        return user.groups.filter(name='Manager').exists()
    
    def get(self, request):
        menu_items = Product.objects.all()
        serializer = ProductSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if self.is_manager(self.request.user):
            serialized_item=ProductSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'mensaje': f'Product {ProductSerializer.fields__title} Created'},status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def patch(self, request):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        return Response(status=status.HTTP_403_FORBIDDEN)


class MenuItemDetailView(APIView):
    pass





















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