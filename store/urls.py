"""
URL patterns for the store app.

This module defines URL patterns using Django's path() function to map views to URLs.

Functions:
    path: Function from django.urls for defining URL patterns.
    views: Module containing view classes for handling HTTP requests.

URL Patterns:
    '' : URL pattern for the main store page.
    'category/<slug:category_slug>/' : URL pattern for browsing products by category.
    'category/<slug:category_slug>/<slug:product_slug>/' : URL pattern for displaying details of a single product.
    'search/' : URL pattern for searching products.
    'gift/<slug:gift_slug>/' : URL pattern for browsing products by gift category.

Attributes:
    views.Store.as_view(): View class for handling store-related requests.
    views.SingleProduct.as_view(): View class for displaying details of a single product.
    views.Search.as_view(): View class for searching products.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.Store.as_view(), name='store'),
    path('category/<slug:category_slug>/', views.Store.as_view(), name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.SingleProduct.as_view(), name='single_product'),
    path('search/', views.Search.as_view(), name='search'),
    path('gift/<slug:gift_slug>/', views.Store.as_view(), name='products_by_gift')
]
