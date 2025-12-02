from .cart import Cart

# Create context processor 
def cart(request):
    # Return the default data from Cart
    return {'cart': Cart(request)}