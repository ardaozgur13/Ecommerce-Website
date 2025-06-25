from .cart import Cart

# Create context processors so our cart can work all pages of site.
def cart(request):
    # Return the default data from the our Cart.
    return {'cart': Cart(request)}