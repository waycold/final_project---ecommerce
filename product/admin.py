from django.contrib import admin
from product.models import Item, OrderItem, Order, Profile

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Profile)