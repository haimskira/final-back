from django.contrib import admin
from .models import Product, Profile, Cart, CartItem, Purchase

admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Purchase)

