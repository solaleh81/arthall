# Importing necessary modules and functions
from django.urls import path  # Function for defining URL patterns
from . import views  # Importing views from the current directory

# URL patterns for cart-related functionality
urlpatterns = [
    # URL pattern for displaying the cart
    path('', views.cart, name='cart'),

    # URL pattern for adding items to the cart
    path('add_cart/<int:product_id>/', views.AddCart.as_view(), name='add_cart'),

    # URL pattern for deleting items from the cart
    path('delete/<int:product_id>/<int:cart_item_id>/', views.DeleteItem.as_view(), name='delete'),

    # URL pattern for the checkout process
    path('checkout/', views.Checkout.as_view(), name='checkout'),
]
