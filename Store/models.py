from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    username = models.CharField(max_length=25)
    email = models.EmailField()


class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(decimal_places=2)
    image = models.FileField(upload_to="product")
    description = models.CharField(max_length=1000)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order, on_delete=models.CASCADE)


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=16)
    address = models.CharField(max_length=1000)
    is_success = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now())
