from django.urls import path, include
from .views import  MenuItems, MenuItemDetailView,Managers,DeliveryCrewView,DeleteDeliveryCrewView,CartView #ManagerSingleView
# from .views import CustomUserListCreateView


urlpatterns = [
    
    path('', include('djoser.urls')),
    path('users/users/me/', include('djoser.urls.authtoken')),
    path('menu-items/', MenuItems.as_view(), name='menu-items'),
    path('menu-items/<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-detail'),
    path('groups/manager/users/', Managers.as_view(), name='manager-view'),
    path('groups/delivery-crew/users',DeliveryCrewView.as_view(), name='delivery-crew-view'),
    path('groups/delivery-crew/users/<int:pk>',DeleteDeliveryCrewView.as_view(), name='delivery-crew-view'),
    path('cart/menu-items', CartView.as_view(),name='cart-view'),
    #path('group/manager/user/<int:pk>/',ManagerSingleView.as_view(), name="namager-single-view")
]