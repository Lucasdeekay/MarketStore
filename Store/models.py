import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    username = models.CharField(max_length=25)
    email = models.EmailField()

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=250)
    image = models.FileField(upload_to="category")
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.FileField(upload_to="product")
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    order_placed = models.BooleanField(default=False)

    def calculate_total_cost(self):
        self.total_amount = sum([
            order.amount for order in self.orders.all()
        ])

    def __str__(self):
        return self.customer.full_name


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=16)
    address = models.CharField(max_length=1000)
    is_success = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.transaction_id
