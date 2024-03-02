"""
Module defining models for the store app.

This module defines Django models representing products, prices, variations, and their relationships.

Classes:
    Price: Model for storing product prices.
    Product: Model for storing product information including name, description, artist, price, etc.
    Variation: Model for storing variations of a product, such as color and size.

Dependencies:
    models: Module from django.db for defining Django models.
    reverse: Function from django.urls for generating URLs.
    Category: Model from category.models for defining product categories.
    GiftCategory: Model from category.models for defining gift categories.

Attributes:
    price: IntegerField representing the price of a product.
    product_name: CharField representing the name of a product.
    slug: SlugField representing the slug of a product for SEO-friendly URLs.
    description: TextField representing the description of a product.
    artist: CharField representing the artist of a product.
    price: ForeignKey representing the price of a product.
    image: ImageField representing the image of a product.
    stock: IntegerField representing the stock quantity of a product.
    is_available: BooleanField representing whether a product is available for purchase.
    category: ForeignKey representing the category of a product.
    gift: ForeignKey representing the gift category of a product.
    created_date: DateTimeField representing the date and time when a product was created.
    modified_date: DateTimeField representing the date and time when a product was last modified.
    get_url(): Method to get the URL of a product.
    VariationManager: Manager class for Variation model providing methods for filtering variations by category.
    variation_category_choice: Choices for the variation category field.
    Variation: Model for storing variations of a product, such as color and size.
"""

from django.db import models
from django.urls import reverse

from category.models import Category, GiftCategory


class Price(models.Model):
    """Model for storing product prices."""
    price = models.IntegerField()

    def __str__(self):
        return f"{self.price}"


class Product(models.Model):
    """Model for storing product information."""
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    artist = models.CharField(max_length=255)
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    gift = models.ForeignKey(GiftCategory, on_delete=models.CASCADE, related_name='products')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        """Method to get the URL of a product."""
        return reverse('single_product', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    """Manager class for Variation model providing methods for filtering variations by category."""

    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    """Model for storing variations of a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
