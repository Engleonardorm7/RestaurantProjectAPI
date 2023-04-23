from rest_framework import generics, status
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models import Q


class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            if not CustomUser.objects.filter(Q(username=username) | Q(email=email)).exists():
                serializer.save()
                return Response({'message': f'User {username} created successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'User with that username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)


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