import string
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from Store.models import Product, Customer, Cart, Order, Transaction, Category

random = random.Random()


# Create your views here.
class LoginView(View):
    template_name = "store/login.html"

    def get(self, request):
        # Go to the register page
        return render(request, self.template_name)

    def post(self, request):
        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            username = request.POST.get("username").strip()
            password = request.POST.get("password")

            # Authenticate user
            user = authenticate(username=username, password=password)

            # Check if user exist
            if user is not None:
                # Login user
                login(request, user)
                # Redirect to learning page
                return HttpResponseRedirect(reverse("Store:home"))
            else:
                # Send error message
                messages.error(request, "Invalid credentials")
                # Redirect to login page
                return HttpResponseRedirect(reverse("Store:login"))


class RegisterView(View):

    def post(self, request):
        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            full_name = request.POST.get("full_name").strip().upper()
            username = request.POST.get("username").strip()
            email = request.POST.get("email").strip()
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password").strip()

            # Check if user with username already exists
            if not User.objects.filter(username=username).exists():
                if password == confirm_password:
                    # Create user and person
                    user = User.objects.create_user(username=username, password=password)
                    customer = Customer.objects.create(user=user, full_name=full_name, username=username, email=email)
                    Cart.objects.create(customer=customer)
                    # Send success message
                    messages.success(request, "Registration successful. Please login")
                    # Redirect to login page
                    return HttpResponseRedirect(reverse("Store:login"))
                else:
                    # Send error message
                    messages.error(request, "Password does not match")
                    # Redirect back to register page
                    return HttpResponseRedirect(reverse("Store:login"))
            else:
                # Send error message
                messages.error(request, "Username already exists")
                # Redirect back to register page
                return HttpResponseRedirect(reverse("Store:login"))


class ForgotPasswordView(View):
    template_name = "store/forgot_password.html"

    def get(self, request):
        # Go to the register page
        return render(request, self.template_name)

    def post(self, request):
        # Collect inputs
        username = request.POST.get("username").strip()

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            customer = Customer.objects.get(user=user)
            return HttpResponseRedirect(reverse("Store:change_password", args=(customer.id,)))
        else:
            messages.error(request, "User does not exist")
            return HttpResponseRedirect(reverse("Store:forgot_password"))


class ChangePasswordView(View):
    template_name = "store/change_password.html"

    def get(self, request, id):
        # Go to the register page
        return render(request, self.template_name)

    def post(self, request, id):
        customer = Customer.objects.get(id=id)

        # Collect inputs
        password = request.POST.get("password").strip()
        confirm_password = request.POST.get("confirm_password").strip()

        if password == confirm_password:
            customer.user.set_password(password)
            customer.user.save()
            messages.success(request, "Password update successful")
            return HttpResponseRedirect(reverse("Store:login"))
        else:
            messages.error(request, "Password does not match")
            return HttpResponseRedirect(reverse("Store:change_password", args=(customer.id,)))


class HomeView(View):
    template_name = "store/home.html"

    def get(self, request):
        all_categories = Category.objects.all()
        context = {"all_categories": all_categories}

        if request.user.is_authenticated and not request.user.is_superuser:
            customer = Customer.objects.get(user=request.user)
            context = {"customer": customer, "all_categories": all_categories}

        return render(request, self.template_name, context=context)


class StoreView(View):
    template_name = "store/store.html"

    def get(self, request, id):
        category = Category.objects.get(id=id)
        products = Product.objects.filter(category=category)
        context = {"products": products}

        if request.user.is_authenticated and not request.user.is_superuser:
            customer = Customer.objects.get(user=request.user)
            context = {"customer": customer, "category": category, "products": products}

        return render(request, self.template_name, context=context)


class ProductView(View):
    template_name = "store/product.html"

    def get(self, request, id):
        product = Product.objects.get(id=id)
        context = {"product": product}

        if request.user.is_authenticated and not request.user.is_superuser:
            customer = Customer.objects.get(user=request.user)
            context = {"customer": customer, "product": product}

        return render(request, self.template_name, context=context)

    @method_decorator(login_required())
    def post(self, request, id):
        quantity = request.POST.get("quantity")

        customer = Customer.objects.get(user=request.user)
        product = Product.objects.get(id=id)
        try:
            cart = Cart.objects.get(customer=customer, order_placed=False)
        except Exception:
            cart = Cart.objects.create(customer=customer)
        amount = float(product.price) * float(quantity)

        if int(quantity) > 0:
            order = Order.objects.create(customer=customer, product=product, quantity=quantity, amount=amount)
            cart.orders.add(order)
            cart.calculate_total_cost()
            cart.save()
            messages.success(request, "Order added to cart")
            return HttpResponseRedirect(reverse("Store:cart"))
        else:
            messages.error(request, "Enter valid quantity")
            return HttpResponseRedirect(reverse("Store:product", args=(product.id,)))


class CartView(View):
    template_name = "store/cart.html"

    @method_decorator(login_required())
    def get(self, request):
        customer = Customer.objects.get(user=request.user)

        try:
            cart = Cart.objects.get(customer=customer, order_placed=False)
        except Exception:
            cart = Cart.objects.create(customer=customer)

        products = []
        total_sum = 0
        try:
            for order in cart.orders.all():
                product = {
                        "id": order.id,
                        "name": order.product.name,
                        "quantity": order.quantity,
                        "amount": order.amount,
                        "price": order.product.price,
                        "image": order.product.image,
                        "description": order.product.description,
                    }
                total_sum += order.amount
                products.append(product)
        except Exception:
            pass
        context = {"customer": customer, "products": products, "total_sum": total_sum}

        return render(request, self.template_name, context=context)


class RemoveOrderView(View):

    @method_decorator(login_required())
    def get(self, request, id):
        order = Order.objects.get(id=id)
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(customer=customer)
        cart.orders.remove(order)
        cart.save()
        messages.success(request, "Order removed from cart")
        return HttpResponseRedirect(reverse("Store:cart"))


class CheckoutView(View):
    template_name = "store/checkout.html"

    @method_decorator(login_required())
    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(customer=customer, order_placed=False)
        products = [
            {
                "id": order.id,
                "name": order.product.name,
                "quantity": order.quantity,
                "amount": order.amount,
                "price": order.product.price,
                "image": order.product.image,
            } for order in cart.orders.all()
        ]
        total_sum = sum([
            order.amount for order in cart.orders.all()
        ])
        context = {"customer": customer, "products": products, "total_sum": total_sum}

        return render(request, self.template_name, context=context)

    @method_decorator(login_required())
    def post(self, request):
        address = request.POST.get("address")

        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(customer=customer, order_placed=False)
        trans_id = ''.join(
            [random.choice(string.ascii_letters + string.digits) for i in range(16)])
        Transaction.objects.create(customer=customer, cart=cart, transaction_id=trans_id, address=address)

        cart.order_placed = True
        cart.save()

        messages.success(request, "Transaction currently awaiting verification")
        return HttpResponseRedirect(reverse("Store:transactions"))


class TransactionView(View):
    template_name = "store/transaction.html"

    @method_decorator(login_required())
    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        transactions = Transaction.objects.filter(customer=customer)
        context = {"customer": customer, "transactions": transactions}

        return render(request, self.template_name, context=context)


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("Store:home"))
