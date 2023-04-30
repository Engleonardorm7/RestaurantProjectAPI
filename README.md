# Django API - Restaurant

This is a Django REST API that allows you to interact with a simple restaurant management system. 

This API provides various functionalities such as user and group creation for Managers, customers, or Delivery crew. Additionally, you can add products to your e-commerce store, and users can buy them. Once a user confirms the purchase, an order is created, which can be assigned to the delivery crew group for order delivery to the customer. In summary, this API is a comprehensive set of tools to manage orders and product shipments in an online store.


## Installation
To run this project, you need to have Python 3 and Django installed on your system.

## Clone the repository:

``` $ git clone https://github.com/<username>/<repo>.git```

```$ cd Restaurant```

## Install the dependencies:

 ```$ pip install -r requirements.txt```

## Run the migrations:

``` $ python manage.py migrate```

## Create a superuser:

``` $ python manage.py createsuperuser```

## Run the development server:

``` $ python manage.py runserver ```

## Usage

You can access to the API endpoints starting from http://localhost:8000/api/.



### Menu Items
**Resource URL**: ```http://localhost:8000/api/menu-items/```

This endpoint allows you to view, create, update, and delete menu items. 
HTTP Methods: GET, POST, PUT, PATCH, DELETE.

* GET: 
Returns a list of all menu items.
Response: A list of serialized menu items.

* POST: 
Creates a new menu item.
Request Body: 
```
{
    "title": "Menu Item Title",
    "price": 50.0,
    "featured": true,
    "category": 1
}
```
Returns the created menu item. 

* PUT: 
Updates an existing menu item.
Request Body: 
```
{
    "title": "New Title",
    "price": 55.0,
    "featured": false,
    "category": 2
}
```
Returns a success message.

* PATCH: 
Partially updates an existing menu item.
Request Body: 
```
{
   "title": "New Title",
}
```
Returns a success message.

* DELETE: 
Deletes an existing menu item.
Response: A success message.

### Menu Item Detail
**Resource URL**: ```http://localhost:8000/api/menu-items/<int:pk>/```

This endpoint allows you to manage a single menu item using the primary key.
HTTP Methods: GET, PUT, PATCH, DELETE.


* GET: 
Returns the serialized menu item.

* PUT: 
Updates the menu item using the specified primary key.
Request Body: 
```
{
    "title": "Menu Item Title",
    "price": 50.0,
    "featured": true,
    "category": 1
}
```
Returns a success message.

* PATCH: 
Partially updates the menu item using the specified primary key.
Request Body: 
```
{
   "title": "New Title"
}
```
Returns a success message.

* DELETE: 
Deletes the menu item with the specified primary key.
Response: A success message.


### Managers
**Resource URL**: ```http://localhost:8000/api/groups/manager/users/```

This endpoint allows managers to view and add users to the "Manager" user group. Only authenticated users belonging to the "Manager" group can access this endpoint. 
HTTP Methods: GET, POST.

* GET: 
Retrieves a list of all the users belonging to the "Manager" group.
Returns a list of serialized users.

* POST: 
Adds a user to the "Manager" group.
Request Body: 
```
{
    "username": "user1"
}
```
Returns a success message.


### Delivery Crew
**Resource URL**: ```http://localhost:8000/api/groups/delivery-crew/users/```

This endpoint allows managers to view and add users to the "Delivery crew" user group. Only authenticated users belonging to the "Manager" group can access this endpoint. 
HTTP Methods: GET, POST, DELETE.

* GET: 
Retrieves a list of all the users belonging to the "Delivery crew" group.
Returns a list of serialized users.

* POST: 
Adds a user to the "Delivery crew" group.
Request Body: 
```
{
    "username": "user1"
}
```
Returns a success message.

* DELETE: 
Removes a user from the "Delivery crew" group.
Request Body: 
```
{
    "username": "user1"
}
```
Returns a success message.


### Users
**Resource URL**: ```http://localhost:8000/api/users/```

This is a built-in django-djoser endpoint that allows you to register new users and authenticate existing users. 
HTTP Methods: GET, POST.

* GET: 
Returns a user's information if the user is currently authenticated.

* POST: 
Creates a new user.


### Cart
**Resource URL**: ```http://localhost:8000/api/cart/menu-items```

This endpoint allows users to view and manage the items in their cart. 
HTTP Methods: GET, POST, DELETE.

* GET: 
Returns a list of all the items in the user's cart.

* POST: 
Adds an item to the user's cart.
Request Body: 
```
{
    "product_id": 1,
    "quantity": 2
}
```
Returns the created cart item.

* DELETE: 
Removes all the items from the user's cart.


### Orders
**Resource URL**: ```http://localhost:8000/api/orders```

This endpoint allows users to create, view, and delete their orders. Managers can view all orders, and delivery crew members can view and update orders assigned to them.

HTTP Methods: GET, POST, DELETE.

* GET: 
Retrieves a list of orders. Managers can view all orders, and delivery crew members can view orders assigned to them. Regular users can only view their own orders. 
Returns a list of serialized orders.

* POST: 
Creates a new order based on the items in the user's cart. Deletes the cart items after the order is created.
Request Body: 
```
{
    "product_id": 1,
    "quantity": 2
}
```
Returns the created order. 

* DELETE: 
Deletes all the existing orders created by the user.

### Order Detail
**Resource URL**: ```http://localhost:8000/api/orders/<int:pk>```

This endpoint allows users to view and manage a single order using the primary key. Managers can view all orders, and delivery crew members can view orders assigned to them.

HTTP Methods: GET, PUT, PATCH, DELETE.

* GET: 
Retrieves a single order using the specified primary key.
Returns the serialized order.

* PUT: 
Updates a single order using the specified primary key.
Request Body: 
```
{
    "delivery_crew": 2,
    "status": true
}
```
Returns a success message.

* PATCH: 
Partially updates a single order using the specified primary key.
Request Body: 
```
{
    "status": true
}
```
Returns a success message.

* DELETE: 
Deletes the order with the specified primary key.
Response: A success message.

## Conclusion

This Django REST API allows you to manage menu items, users, and orders in a restaurant. You can use it to create, read, update, and delete data through HTTP methods.
