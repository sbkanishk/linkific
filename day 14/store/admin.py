from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review

# Register everything so you can manage your whole store from the dashboard!
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)