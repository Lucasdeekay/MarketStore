from django.contrib import admin

from Store.models import Customer, Product, Cart, Order, Transaction


# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'username', 'email')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image', 'description')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('customer',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'is_success', 'date')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
