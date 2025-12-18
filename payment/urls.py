from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("payment/", views.payment, name="payment"),
    path("payment_success/", views.payment_success, name="payment_success"),


]