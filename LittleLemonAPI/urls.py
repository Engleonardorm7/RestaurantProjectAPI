from django.urls import path, include
from .views import  ManagersView, MenuItems, MenuItemDetailView,Managers
# from .views import CustomUserListCreateView


urlpatterns = [
    
    path('', include('djoser.urls')),
    path('users/users/me/', include('djoser.urls.authtoken')),

    path('groups/manager/users/', Managers.as_view(), name='manager-view'),
    #path('menu-items/', MenuItemsList.as_view(), name='menu-items'),
    path('menu-items/', MenuItems.as_view(), name='menu-items'),
    # path('menu-items/', MenuItemListView.as_view(), name='menuitem-list'),
    path('menu-items/<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-detail'),
]