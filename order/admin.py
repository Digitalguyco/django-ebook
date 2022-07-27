from django.contrib import admin

from .models import Order,OrderItem

#  Orderitem To be inline In OrderAdmin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','status','created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name','address']
    inlines = [OrderItemInline] # Inline

# Regiter Order and Orderitem
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)