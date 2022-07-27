from django.db import models
from django.contrib.auth.models import User

from product.models import Product

class Order(models.Model):
    ORDERED = 'ordered'
    DELIVERED = 'devlivered'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (DELIVERED, 'delivered')
    )

    user = models.ForeignKey(User, related_name='orders', blank=True, null=True, on_delete=models.CASCADE) # FK User Model
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    payment_intent = models.CharField(max_length=300) # stripe payment intent
    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

    class Meta:
        ordering = ('-created_at',)
    
    def get_total_price(self):
        if self.paid_amount:
            return self.paid_amount / 100 # Price divide by 100
        
        return 0

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE) # FK Order
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE) # FK Product
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.price / 100 # Price divide by 100