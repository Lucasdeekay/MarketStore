from django.contrib import admin

from Store.models import Customer, Product, Cart, Order, Transaction, Category


# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'username', 'email')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'image', 'description')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'amount')


class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_amount', 'order_placed')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'cart', 'transaction_id', 'address', 'is_success', 'date')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
