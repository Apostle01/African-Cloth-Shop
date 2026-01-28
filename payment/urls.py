from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("payment/", views.payment, name="payment"),
    path("payment_success/", views.payment_success, name="payment_success"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("orders/", views.order_history, name="order_history"),
    path("webhook/", views.stripe_webhook, name="stripe_webhook"),
]