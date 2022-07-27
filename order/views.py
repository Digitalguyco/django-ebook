from django.shortcuts import render

import json
import stripe

from django.conf import settings
from django.http import JsonResponse

from cart.cart import Cart

from .models import Order, OrderItem

# Start Order View
def start_order(request):
    cart = Cart(request) # Cart Instance
    data = json.loads(request.body)
    total_price = 0

    items = [] # items
    YOUR_URL = 'https://djebook.herokuapp.com'

    for item in cart: # loop The cart instance
        product = item['product']
        total_price += product.price * int(item['quantity'])

        items.append({
            'price_data': {
                'currency': 'usd',
                'product_data':{
                    'name': product.name,
                },
                'unit_amount': product.price,
            },
            'quantity': item['quantity']
        }
        ) # apped data ot items 

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN # Stripe  SECRET ACCESS KEY
    session  = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = items,
        mode='payment',
        success_url = f'{YOUR_URL}/cart/success/',
        cancel_url =f'{YOUR_URL}/cart/'
    ) # Creating Checkout Session
    payment_intent = session.payment_intent # Payment 

    order = Order.objects.create(
        user = request.user,
        first_name = data['first_name'],
        last_name=data['last_name'], 
        email=data['email'], 
        phone=data['phone'], 
        address=data['address'], 
        zipcode=data['zipcode'], 
        place=data['place'],
        payment_intent=payment_intent,
        paid=True,
        paid_amount=total_price
    ) # Creating Oreder

    for item in cart:
        product = item['product']
        quantity = int(item['quantity'])
        price = product.price * quantity

        item = OrderItem.objects.create(
            order=order, 
            product=product, 
            price=price, 
            quantity=quantity
        ) # Creating OrderItem

    cart.clear() # Clear Cart 

    return JsonResponse({'session': session, 'order':payment_intent}) # Return for Js side.