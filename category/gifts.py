from category.models import GiftCategory


def gifts(request):
    """
    Function to retrieve gift category links.

    Args:
        request: HttpRequest object representing the HTTP request.

    Returns:
        dict: A dictionary containing gift category links.
    """
    # Retrieve all gift category objects
    gifts = GiftCategory.objects.all()
    return dict(gifts=gifts)