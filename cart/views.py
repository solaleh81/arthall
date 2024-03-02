from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from store.models import Product, Variation
from django.utils.decorators import method_decorator


def _cart_id(request):
    """
       Function to retrieve the session key for the cart.

       Args:
           request: HttpRequest object representing the HTTP request.

       Returns:
           str: The session key for the cart.
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


class AddCart(APIView):
    """
        API view for adding items to the cart.
    """

    # POST method for adding items to the cart
    def post(self, request, product_id):
        """
            POST method for adding items to the cart.

            Args:
                request: HttpRequest object representing the HTTP request.
                product_id: The ID of the product being added to the cart.

            Returns:
                HttpResponseRedirect: Redirects to the cart page after adding the item.
        """
        # Implementation of adding items to the cart
        # (code omitted for brevity)

        current_user = request.user
        product = get_object_or_404(Product, id=product_id)
        # if the user is authenticated
        if current_user.is_authenticated:
            product_variation = []
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id=_cart_id(request)
                )
            cart.save()

            is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(product=product, user=current_user)
                # print(cart_items)
                ex_var_list = []
                id = []
                for item in cart_item:
                    existing_variation = item.variation.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)
                    # print(ex_var_list)
                if product_variation in ex_var_list:
                    index = ex_var_list.index(product_variation)
                    item_id = id[index]
                    item = CartItem.objects.get(product=product, id=item_id)
                    item.quantity += 1
                    item.save()
                else:
                    cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                    if len(product_variation) > 0:
                        for item in product_variation:
                            cart_item.variation.add(item)
                    # cart_item.quantity += 1
                    cart_item.product.stock -= 1
                    cart_item.product.save()
                    cart_item.save()
            else:

                cart_item = CartItem.objects.create(product=product, user=current_user, quantity=1)

                if len(product_variation) > 0:
                    for item in product_variation:
                        cart_item.variation.add(item)
                cart_item.save()
            return redirect('cart')
        # if the user is not authenticated
        else:
            product_variation = []
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id=_cart_id(request)
                )
            cart.save()

            is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(product=product, cart=cart)
                # print(cart_items)
                ex_var_list = []
                id = []
                for item in cart_item:
                    existing_variation = item.variation.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)
                    # print(ex_var_list)
                if product_variation in ex_var_list:
                    index = ex_var_list.index(product_variation)
                    item_id = id[index]
                    item = CartItem.objects.get(product=product, id=item_id)
                    item.quantity += 1
                    item.save()
                else:
                    cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
                    if len(product_variation) > 0:
                        for item in product_variation:
                            cart_item.variation.add(item)
                    # cart_item.quantity += 1
                    cart_item.product.stock -= 1
                    cart_item.product.save()
                    cart_item.save()
            else:
                cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)

                if len(product_variation) > 0:
                    for item in product_variation:
                        cart_item.variation.add(item)
                cart_item.save()
            return redirect('cart')

    # GET method for adding items to the cart
    def get(self, request, product_id):
        """
               GET method for adding items to the cart.

               Args:
                   request: HttpRequest object representing the HTTP request.
                   product_id: The ID of the product being added to the cart.

               Returns:
                   HttpResponseRedirect: Redirects to the cart page after adding the item.
        """
        # Implementation of adding items to the cart
        # (code omitted for brevity)
        product = get_object_or_404(Product, id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.product.stock -= 1
            cart_item.product.save()
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            cart_item.save()
        return redirect('cart')


class DeleteItem(APIView):
    """
       API view for deleting items from the cart.
    """
    # GET method for deleting items from the cart
    def get(self, request, product_id, cart_item_id):
        """
                GET method for deleting items from the cart.

                Args:
                    request: HttpRequest object representing the HTTP request.
                    product_id: The ID of the product being deleted from the cart.
                    cart_item_id: The ID of the cart item being deleted.

                Returns:
                    HttpResponseRedirect: Redirects to the cart page after deleting the item.
        """
        # Implementation of deleting items from the cart
        # (code omitted for brevity)
        product = get_object_or_404(Product, id=product_id)

        try:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            pass
        return redirect('cart')


def cart(request, total=0, quantity=0, cart_item=None):
    """
        Function-based view for displaying the cart.

        Args:
            request: HttpRequest object representing the HTTP request.
            total (int): The total price of items in the cart.
            quantity (int): The total quantity of items in the cart.
            cart_item: The cart item being displayed.

        Returns:
            HttpResponse: Renders the cart template with cart data.
    """
    # Implementation of displaying the cart
    # (code omitted for brevity)
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            print(request.user.is_authenticated)
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            print(cart_items)
        else:
            cart = get_object_or_404(Cart, cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price.price * cart_item.quantity)
            quantity = cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except CartItem.DoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context=context)

# Class-based view for checkout process
@method_decorator(login_required(login_url='login'), name='dispatch')
class Checkout(APIView):
    """
       Class-based view for the checkout process.
    """

    # GET method for the checkout process
    def get(self, request, total=0, quantity=0, cart_item=None, current_user=None):
        """
                GET method for the checkout process.

                Args:
                    request: HttpRequest object representing the HTTP request.
                    total (int): The total price of items in the cart.
                    quantity (int): The total quantity of items in the cart.
                    cart_item: The cart item being displayed.
                    current_user: The current authenticated user.

                Returns:
                    HttpResponse: Renders the checkout template with checkout data.
        """
        # Implementation of the checkout process
        # (code omitted for brevity)
        try:
            tax = 0
            grand_total = 0
            if request.user.is_authenticated:
                print(request.user.is_authenticated)
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
                print(cart_items)
            else:
                cart = get_object_or_404(Cart, cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price.price * cart_item.quantity)
                quantity = cart_item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax
        except CartItem.DoesNotExist:
            pass
        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': grand_total,
        }

        return render(request, 'store/checkout.html', context=context)


