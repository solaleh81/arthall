# Importing necessary modules for handling signals
from django.db.models.signals import post_save  # Signal for post-save events on models
from django.dispatch import receiver  # Decorator for connecting receivers to signals

# Importing the Order model from the orders app
from orders.models import Order  # Model representing an order

# Importing the send_order_sms task from the current directory
from .tasks import send_order_sms  # Task for sending order confirmation SMS

# Define a receiver to handle post-save events on the Order model
@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    """
    Receiver function to handle post-save events on the Order model.

    Args:
        sender: The sender model class.
        instance: The actual instance being saved.
        created: A boolean indicating whether the instance was created.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    # If the instance is newly created, send an order confirmation SMS asynchronously
    if created:
        send_order_sms.delay(instance.id)
