# Importing necessary modules
import datetime


from django.http import HttpResponse  # Class for returning HTTP responses
from django.shortcuts import render, redirect
from rest_framework.views import APIView

# Importing models from the application
from cart.models import CartItem
from orders.models import Order

# Define an APIView for placing orders
class PlaceOrder(APIView):
    """
    APIView for handling the placement of orders.
    """

    def post(self, request, total=0, quantity=0):
        """
        Handles POST requests for placing orders.

        Args:
            request: HttpRequest object representing the HTTP request.
            total: Optional variable representing the total price of the order.
            quantity: Optional variable representing the total quantity of items in the order.

        Returns:
            HttpResponse object with the rendered HTML template displaying payment details.
        """
        # Get the current authenticated user
        current_user = request.user

        # Retrieve cart items for the current user
        cart_items = CartItem.objects.filter(user=current_user)

        # Count the number of items in the cart
        count = cart_items.count()

        # Redirect to the store if the cart is empty
        if count <= 0:
            return redirect('store')

        # Initialize variables for total price and quantity
        grand_total = 0
        tax = 0

        # Calculate the total price and quantity of items in the cart
        for cart_item in cart_items:
            total += (cart_item.product.price.price * cart_item.quantity)
            quantity = cart_item.quantity

        # Calculate tax (assumed to be 2% of the total price)
        tax = (2 * total) / 100
        grand_total = total + tax

        # Extract customer information from the POST request
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        order_note = request.POST['order_note']
        ip = request.META.get("REMOTE_ADDR")

        # Check if required data is present in the POST request
        data = {'first_name', 'last_name', 'email', 'phone', 'address_line_1', 'address_line_2', 'city', 'state', 'country', 'order_note'}
        if data:
            # Create a new order instance
            order = Order.objects.create(first_name=first_name, last_name=last_name,
                                         email=email, phone=phone, address_line_1=address_line_1,
                                         address_line_2=address_line_2, city=city,
                                         state=state, country=country, order_note=order_note,
                                         order_total=grand_total, tax=tax, ip=ip, user=current_user,
                                         )
            order.save()

            # Generate an order number based on the current date and order ID
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(order.id)
            order.order_number = order_number
            order.save()

            # Retrieve the created order
            order = Order.objects.get(user=current_user, is_ordered=True, order_number=order_number)

            # Prepare data to be passed to the template
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total
            }

            # Render the payments template with the provided context
            return render(request, 'orders/payments.html', context=context)

        else:
            # Redirect to the checkout page if required data is missing
            return redirect('checkout')
