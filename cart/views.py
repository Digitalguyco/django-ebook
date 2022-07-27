import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .cart import Cart

from product.models import Product


# FBV

# add to cart view
def add_to_cart(request, product_id):
    cart = Cart(request) # Cart instance
    cart.add(product_id) # call cart method add and passing product via product id

    return render(request, 'cart/add-ons/menu_cart.html')


#  CART View
def cart(request):
    return render(request, 'cart/cart.html')

# Sucess View
def success(request):
    return render(request, 'cart/success.html') 

#  Update cart view
def update_cart(request, product_id, action):
    cart = Cart(request) # Cart instance

    if action == 'increment': # if action is increment
        cart.add(product_id, 1, True) # call cart method add and pass product id, quantity 1 and set Update to true
    else: # if decrement 
        cart.add(product_id, -1, True) # call cart method add and pass product id, quantity -1 and set Update to true
    
    product = Product.objects.get(pk=product_id) # Get product by it's id
    quantity = cart.get_item(product_id) # call the get_item method and pass the product id 
    
    if quantity: # if there is a product
        quantity = quantity['quantity'] # get the quantitu
        

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price,
            },
            'total_price': (quantity * product.price / 100),
            'quantity': quantity,
        } # pass product into item 
        
    else:
        item = None
  

    response = render(request, 'cart/add-ons/cart_item.html', {'item': item})
    response['HX-Trigger'] = 'update-menu-cart'

    return response


# Checkout view
@login_required
def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE # Stripe Pub key
    return render(request, 'cart/checkout.html', {'pub_key': pub_key})

# Menu cart 
def hx_menu_cart(request):
    return render(request, 'cart/add-ons/menu_cart.html')

#  Menu total
def hx_cart_total(request):
    return render(request, 'cart/add-ons/cart_total.html')


