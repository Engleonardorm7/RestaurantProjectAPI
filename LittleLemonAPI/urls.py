from django.urls import path, include
from .views import  ManagersView, MenuItems, MenuItemDetailView,Managers #ManagerSingleView
# from .views import CustomUserListCreateView


urlpatterns = [
    
    path('', include('djoser.urls')),
    path('users/users/me/', include('djoser.urls.authtoken')),
    path('menu-items/', MenuItems.as_view(), name='menu-items'),
    path('menu-items/<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-detail'),
    path('groups/manager/users/', Managers.as_view(), name='manager-view'),
    #path('group/manager/user/<int:pk>/',ManagerSingleView.as_view(), name="namager-single-view")
]