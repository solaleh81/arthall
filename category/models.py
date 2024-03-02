# Importing necessary module for defining Django models
from django.db import models  # Module for defining Django models

# Importing reverse function from django.urls
from django.urls import reverse  # Function for reversing URLs

# Define a model for representing product categories
class Category(models.Model):
    """
    Model for representing product categories.

    Attributes:
        category_name: CharField representing the name of the category.
        slug: SlugField representing the slugified version of the category name.
        description: TextField representing the description of the category.
        cat_image: ImageField representing the image associated with the category.

    Methods:
        get_url: Method to return the URL for viewing products in this category.
        __str__: Method to return a string representation of the category.
    """

    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_url(self):
        """
        Method to return the URL for viewing products in this category.

        Returns:
            String: The URL for viewing products in this category.
        """
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        """
        Method to return a string representation of the category.

        Returns:
            String: The name of the category.
        """
        return self.category_name

# Define a model for representing gift categories
class GiftCategory(models.Model):
    """
    Model for representing gift categories.

    Attributes:
        gift_name: CharField representing the name of the gift category.
        slug: SlugField representing the slugified version of the gift category name.
        description: TextField representing the description of the gift category.
        gift_image: ImageField representing the image associated with the gift category.

    Methods:
        get_url: Method to return the URL for viewing products in this gift category.
        __str__: Method to return a string representation of the gift category.
    """

    gift_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    gift_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'Gift'
        verbose_name_plural = 'Gift Categories'

    def get_url(self):
        """
        Method to return the URL for viewing products in this gift category.

        Returns:
            String: The URL for viewing products in this gift category.
        """
        return reverse('products_by_gift', args=[self.slug])

    def __str__(self):
        """
        Method to return a string representation of the gift category.

        Returns:
            String: The name of the gift category.
        """
        return self.gift_name
