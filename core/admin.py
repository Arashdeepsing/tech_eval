from django.contrib import admin


from .models import Product, Cart, CartItem, Wishlist, WishlistItem,Order, OrderItem

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(Order)
admin.site.register(OrderItem)
