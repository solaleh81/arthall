# Importing models for Category and GiftCategory from the current directory
from .models import Category, GiftCategory

def menu_links(request):
    """
    Function to retrieve category links for the menu.

    Args:
        request: HttpRequest object representing the HTTP request.

    Returns:
        dict: A dictionary containing category links.
    """
    # Retrieve all category objects
    links = Category.objects.all()
    return dict(links=links)

# def gifts(request):
#     """
#     Function to retrieve gift category links.
#
#     Args:
#         request: HttpRequest object representing the HTTP request.
#
#     Returns:
#         dict: A dictionary containing gift category links.
#     """
#     # Retrieve all gift category objects
#     gifts = GiftCategory.objects.all()
#     return dict(links=gifts)
