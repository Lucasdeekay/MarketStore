from django.urls import path

from Store.views import HomeView, ProductView, CartView, CheckoutView, TransactionView

app_name = "Store"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login", HomeView.as_view(), name="login"),
    path("register", HomeView.as_view(), name="register"),
    path("forget_password", HomeView.as_view(), name="forget_password"),
    path("forget_password/<int:id>/change_password", HomeView.as_view(), name="change_password"),
    path("product/<int:id>", ProductView.as_view(), name="product"),
    path("cart", CartView.as_view(), name="cart"),
    path("cart/<int:id>/remove_order", RemoveOrderView, name="remove_order"),
    path("cart/checkout", CheckoutView.as_view(), name="checkout"),
    path("transactions", TransactionView.as_view(), name="transactions"),
]