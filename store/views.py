"""
This module provides views for interacting with the store, including browsing products,
viewing individual product details, and searching for products.

Classes:
    Store: APIView for browsing products, optionally filtered by category and price range.
    SingleProduct: APIView for displaying details of a single product.
    Search: APIView for searching products based on a keyword.

Dependencies:
    Django: The web framework used for developing the application.
    Paginator: Paginator class from django.core.paginator for paginating querysets.
    Q: Q class from django.db.models for complex query lookups.
    HttpResponse: HttpResponse class from django.http for returning HTTP responses.
    render: Function from django.shortcuts for rendering HTML templates.
    get_object_or_404: Function from django.shortcuts for retrieving objects or raising a 404 error if not found.
    APIView: Base class from rest_framework.views for defining API views.

Attributes:
    _cart_id: Function from cart.views for getting the cart ID.
    Category: Model from category.models for defining product categories.
    Product: Model from store.models for defining products.
    Price: Model from store.models for defining product prices.
    Cart: Model from cart.models for defining shopping carts.
    CartItem: Model from cart.models for defining items in the shopping cart.
"""

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView

from cart.views import _cart_id
from category.models import Category
from store.models import Product, Price
from cart.models import Cart, CartItem


class Store(APIView):
    """
    APIView for browsing products in the store, optionally filtered by category and price range.
    """

    def get(self, request, category_slug=None):
        """
        Handles GET requests for browsing products.

        Args:
            request: HttpRequest object representing the HTTP request.
            category_slug: Optional slug of the category to filter products by.

        Returns:
            HttpResponse object with the rendered HTML template displaying products.
        """
        cats = Category.objects.all()
        products = Product.objects.filter(is_available=True).order_by('id')
        prices = Price.objects.all()
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        if min_price is not None and max_price is not None:
            products = products.filter(price__price__range=(min_price, max_price))

        paginator = Paginator(products, 1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        product_count = products.count()

        return render(request, 'store/store.html', {'products': page_obj, 'product_count': product_count,
                                                    'cats': cats, 'prices': prices})


class SingleProduct(APIView):
    """
    APIView for displaying details of a single product.
    """

    def get(self, request, category_slug, product_slug):
        """
        Handles GET requests for displaying details of a single product.

        Args:
            request: HttpRequest object representing the HTTP request.
            category_slug: Slug of the category containing the product.
            product_slug: Slug of the product.

        Returns:
            HttpResponse object with the rendered HTML template displaying product details.
        """
        try:
            category = get_object_or_404(Category, slug=category_slug)
            product = get_object_or_404(Product, category=category, slug=product_slug)
            in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
        except Exception as e:
            raise e

        return render(request, 'store/product-detail.html', {'category': category, 'product': product,
                                                             'in_cart': in_cart})


class Search(APIView):
    """
    APIView for searching products based on a keyword.
    """

    def get(self, request):
        """
        Handles GET requests for searching products based on a keyword.

        Args:
            request: HttpRequest object representing the HTTP request.

        Returns:
            HttpResponse object with the rendered HTML template displaying search results.
        """
        keyword = request.GET.get("keyword")
        if keyword:
            products = Product.objects.filter(Q(product_name__icontains=keyword) | Q(artist__icontains=keyword) |
                                              Q(variations__variation_value__icontains=keyword))
            products = products.distinct().order_by('-id')
            paginator = Paginator(products, 1)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            product_count = products.count()

            context = {'products': products,
                   'product_Count': product_count}
            return render(request, 'store/store.html', context)
