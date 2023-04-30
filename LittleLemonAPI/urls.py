from django.urls import path, include
<<<<<<< HEAD
from .views import  MenuItems, MenuItemDetailView,Managers,DeliveryCrewView,DeleteDeliveryCrewView,CartView #ManagerSingleView
=======
from .views import  MenuItems, MenuItemDetailView,Managers,DeliveryCrewView,DeleteDeliveryCrewView,CartView,OrderView,OrderDetailView #ManagerSingleView
>>>>>>> 9dca2ad
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
    path('orders', OrderView.as_view(), name='orders-view'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='orders-view'),
    #path('group/manager/user/<int:pk>/',ManagerSingleView.as_view(), name="namager-single-view")
]