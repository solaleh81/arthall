# Importing models and functions from the current package
from .models import Cart, CartItem  # Importing models for Cart and CartItem
from .views import _cart_id  # Importing function for retrieving cart ID

def counter(request):
    """
    Counts the number of items in the user's shopping cart.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing the count of items in the shopping cart.
    """
    cart_count = 0
    # Check if the current path is not in the admin section
    if 'admin' in request.path:
        return {}
    else:
        try:
            # Try to retrieve the cart and cart items
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            # Calculate the total number of items in the cart
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
