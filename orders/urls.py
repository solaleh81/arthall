# Importing necessary module for defining URL patterns
from django.urls import path  # Function for defining URL patterns

# Importing views from the current directory
from . import views  # Module containing view classes for handling HTTP requests

# Define URL patterns for the orders app
urlpatterns = [
    # URL pattern for placing an order
    path('place-order/', views.PlaceOrder.as_view(), name='place_order'),
]
