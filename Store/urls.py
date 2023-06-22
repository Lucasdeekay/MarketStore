from django.contrib.auth.views import LogoutView
from django.urls import path

from Store.views import HomeView, ProductView, CartView, CheckoutView, TransactionView, RemoveOrderView, StoreView, \
    LoginView, RegisterView, ForgotPasswordView, ChangePasswordView

app_name = "Store"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("logout", LogoutView.as_view(), name="login"),
    path("forget_password", ForgotPasswordView.as_view(), name="forget_password"),
    path("forget_password/<int:id>/change_password", ChangePasswordView.as_view(), name="change_password"),
    path("store/<int:id>", StoreView.as_view(), name="store"),
    path("store/product/<int:id>", ProductView.as_view(), name="product"),
    path("cart", CartView.as_view(), name="cart"),
    path("cart/<int:id>/remove_order", RemoveOrderView, name="remove_order"),
    path("cart/checkout", CheckoutView.as_view(), name="checkout"),
    path("transactions", TransactionView.as_view(), name="transactions"),
]