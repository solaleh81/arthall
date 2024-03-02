# Importing necessary modules and functions
from django.contrib.auth import get_user_model  # Function to retrieve the User model
from django.db import models  # Module for defining database models
from store.models import Product, Variation  # Importing models for Product and Variation
from account.models import Account  # Importing model for Account

# Retrieving the User model
user = get_user_model()

# Model for representing a shopping cart
class Cart(models.Model):
    """
    Model for representing a shopping cart.

    Attributes:
        cart_id (str): The ID of the cart.
        date_added (DateTimeField): The date and time when the cart was created.
    """

    cart_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the cart.

        Returns:
            str: The ID of the cart.
        """
        return self.cart_id

# Model for representing an item in the shopping cart
class CartItem(models.Model):
    """
    Model for representing an item in the shopping cart.

    Attributes:
        user (ForeignKey): The user associated with the cart item.
        product (ForeignKey): The product added to the cart.
        variation (ManyToManyField): The variations of the product.
        cart (ForeignKey): The cart to which the item belongs.
        quantity (int): The quantity of the product in the cart.
        is_active (bool): Indicates whether the item is active or not.
    """

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="cart_items", null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    variation = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='carts', null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        """
        Calculates the subtotal for the cart item.

        Returns:
            float: The subtotal for the cart item.
        """
        return self.product.price.price * self.quantity

    def __str__(self):
        """
        Returns a string representation of the cart item.

        Returns:
            str: The name of the product.
        """
        return f'{self.product.product_name}'
