This is an E-Commerce website built using Django, a high-level Python web framework. The website allows users to register, login, browse products, add them to the cart, and place orders.

Features
User Registration: Users can register for an account by providing their details such as name, email, and password.

User Authentication: Registered users can login to their account securely using their email and password.

Product Management: Products are managed by the admin through the Django admin interface. Each product has a name, description, price, and image.

Cart Functionality: Users can add products to their cart, view their cart, and delete items from the cart.

Order Placement: Users can place orders for the products in their cart. They can provide their shipping details during the checkout process.

User Roles: Users have different roles such as normal user, admin, and superuser. Each role has different permissions and access levels.



Installation:

git clone git@github.com:solaleh81/arthall.git

docker exec -it arthall-web-1 /bin/bash

python manage.py makemigrations

python manage.py migrate

Access the website at http://localhost:8001/

Usage
Visit the registration page to create a new account.
Login to your account using your email and password.
Browse products, add them to your cart, and proceed to checkout to place an order.
As an admin, you can manage products and orders through the Django admin interface.


you can access django admin for this site with:

http://localhost:8001/admin/