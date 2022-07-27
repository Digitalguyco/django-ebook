from .cart import Cart

# Manage Cart
def cart(request):
    return {'cart': Cart(request)} # Cart Instance