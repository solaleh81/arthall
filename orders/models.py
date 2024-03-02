# Importing necessary module for defining Django models
from django.db import models  # Module for defining Django models

# Importing the Account model from the account app
from account.models import Account  # Model representing user accounts

# Define a model for representing orders
class Order(models.Model):
    """
    Model for representing orders.

    Attributes:
        STATUS: Choices for the status of the order.
        user: ForeignKey representing the user who placed the order.
        order_number: CharField representing the unique order number.
        first_name: CharField representing the first name of the customer.
        last_name: CharField representing the last name of the customer.
        phone: CharField representing the phone number of the customer.
        email: CharField representing the email address of the customer.
        address_line_1: CharField representing the first line of the customer's address.
        address_line_2: CharField representing the second line of the customer's address.
        country: CharField representing the country of the customer's address.
        state: CharField representing the state of the customer's address.
        city: CharField representing the city of the customer's address.
        order_note: CharField representing any additional notes for the order.
        order_total: FloatField representing the total price of the order.
        tax: CharField representing the tax amount for the order.
        status: CharField representing the status of the order.
        ip: CharField representing the IP address of the customer.
        is_ordered: BooleanField indicating whether the order has been placed.
        created_at: DateTimeField representing the date and time when the order was created.
        updated_at: DateTimeField representing the date and time when the order was last updated.

    Methods:
        __str__: Method to return a string representation of the order.
        full_name: Method to return the full name of the customer.
        full_address: Method to return the full address of the customer.
    """

    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="orders")
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Method to return a string representation of the order.

        Returns:
            String: A formatted string representing the order.
        """
        return f"{ self.user.first_name}-{self.user.phone_number}"

    def full_name(self):
        """
        Method to return the full name of the customer.

        Returns:
            String: The full name of the customer.
        """
        return f"{self.first_name} {self.last_name}"

    def full_address(self):
        """
        Method to return the full address of the customer.

        Returns:
            String: The full address of the customer.
        """
        return f"{self.address_line_1} {self.address_line_2}"
