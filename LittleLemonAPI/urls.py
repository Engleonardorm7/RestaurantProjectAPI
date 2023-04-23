from django.urls import path
from djoser.views import TokenCreateView, TokenDestroyView
from .views import UserDetailsView, ManagersView

from .views import CustomUserListCreateView
from rest_framework.authtoken.views import obtain_auth_token
#from .views import MenuItemListView, MenuItemDetailView
urlpatterns = [
    path('users/', CustomUserListCreateView.as_view(), name='user-create'),
    path('token/login/', obtain_auth_token, name='token-create'),
    path('token/logout/', TokenDestroyView.as_view(), name='token-destroy'),
    path('users/users/me/', UserDetailsView.as_view(),name='users-me'),
    path('groups/manager/users', ManagersView.as_view(), name='manager-view')
    # path('menu-items/', MenuItemListView.as_view(), name='menuitem-list'),
    # path('menu-items/<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-detail'),
]