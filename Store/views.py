import string
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from Store.models import Product, Customer, Cart, Order, Transaction

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
    template_name = "store/register.html"

    def get(self, request):
        # Go to the register page
        return render(request, self.template_name)

    def post(self, request):
        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            full_name = request.POST.get("full_name").strip().capitalize()
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
                    return HttpResponseRedirect(reverse("Store:register"))
            else:
                # Send error message
                messages.error(request, "Username already exists")
                # Redirect back to register page
                return HttpResponseRedirect(reverse("Store:register"))


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
            return HttpResponseRedirect(reverse("Assignment:login"))
        else:
            messages.error(request, "Password does not match")
            return HttpResponseRedirect(reverse("Assignment:change_password", args=(customer.id,)))


class HomeView(View):
    template_name = "store/home.html"

    def get(self, request):
        all_products = Product.objects.all()
        context = {"all_products": all_products}

        if request.user.is_authenticated() and not request.user.is_superuser():
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.get(customer=customer)
            context = {"customer": customer, "cart": cart, "all_products": all_products}

        return render(request, self.template_name, context=context)


class ProductView(View):
    template_name = "store/product.html"

    def get(self, request, id):
        product = Product.objects.get(id=id)
        context = {"product": product}

        if request.user.is_authenticated() and not request.user.is_superuser():
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.get(customer=customer)
            context = {"customer": customer, "cart": cart, "product": product}

        return render(request, self.template_name, context=context)

    @method_decorator(login_required())
    def post(self, request, id):
        quantity = request.POST.get("quantity")

        customer = Customer.objects.get(user=request.user)
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(customer=customer)

        if quantity > 0:
            order = Order.objects.create(customer=customer, product=product, quantity=quantity)
            cart.orders.add(order)
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
        cart = Cart.objects.get(customer=customer)
        context = {"customer": customer, "cart": cart}

        return render(request, self.template_name, context=context)


class RemoveOrderView(View):

    @method_decorator(login_required())
    def post(self, request, id):
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
        cart = Cart.objects.get(customer=customer)
        context = {"customer": customer, "cart": cart}

        return render(request, self.template_name, context=context)

    @method_decorator(login_required())
    def post(self, request):
        address = request.POST.get("address")

        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(customer=customer)
        trans_id = ''.join(
            [random.choice(string.ascii_letters + string.digits) for i in range(16)])
        Transaction.objects.create(customer=customer, cart=cart, transaction_id=trans_id, address=address)
        messages.success(request, "Transaction currently awaiting verification")
        return HttpResponseRedirect(reverse("Store:transaction"))


class TransactionView(View):
    template_name = "store/transaction.html"

    @method_decorator(login_required())
    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        transactions = Transaction.objects.filter(customer=customer)
        context = {"transactions": transactions}

        return render(request, self.template_name, context=context)
