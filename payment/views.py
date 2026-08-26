import os
import stripe
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cart.cart import Cart
from .models import Order, OrderItem, ShippingAddress
from .forms import ShippingForm
from products.models import Product
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY


# @login_required
def checkout(request):
    cart = Cart(request)

    # Make sure the cart is not empty
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart_summary")

    # Get saved shipping address only for authenticated users
    shipping_address = None

    if request.user.is_authenticated:
        shipping_address = ShippingAddress.objects.filter(
            user=request.user
        ).first()

    # Handle submitted checkout form
    if request.method == "POST":

        if request.user.is_authenticated:
            form = ShippingForm(
                request.POST,
                instance=shipping_address
            )
        else:
            # Guest checkout
            form = ShippingForm(request.POST)

        if form.is_valid():

            shipping = form.save(commit=False)

            # Attach the shipping address to the user
            # only when the customer is logged in.
            if request.user.is_authenticated:
                shipping.user = request.user

            shipping.save()

            return redirect("payment:payment")

    else:

        if request.user.is_authenticated:
            form = ShippingForm(
                instance=shipping_address
            )
        else:
            # Empty form for guest customers
            form = ShippingForm()

    # Get current cart items
    cart_items = cart.get_items()

    context = {
        "form": form,
        "cart_items": cart_items,
        "cart_total": cart.get_total(),
    }

    return render(
        request,
        "payment/checkout.html",
        context
    )

def payment(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("cart_summary")

    stripe.api_key = settings.STRIPE_SECRET_KEY

    amount = int(cart.get_total() * 100)

    if request.user.is_authenticated:
        metadata = {
            "user_id": str(request.user.id)
        }
    else:
        metadata = {
            "user_id": "guest"
        }

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency="usd",
        payment_method_types=["card"],
        metadata=metadata
    )

    return render(request, "payment/payment.html", {
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
        "client_secret": intent.client_secret,
        "site_url": settings.SITE_URL,
        "cart": cart,
        "total": cart.get_total(),
    })

def payment_success(request):

    cart = Cart(request)

    # Get the Stripe PaymentIntent ID
    payment_intent = request.GET.get("payment_intent")

    if not payment_intent:
        messages.error(request, "Payment could not be verified.")
        return redirect("cart_summary")

    # Verify the payment with Stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent)
    except stripe.error.StripeError:
        messages.error(
            request,
            "There was a problem verifying your payment."
        )
        return redirect("cart_summary")

    # Make sure Stripe confirms successful payment
    if intent.status != "succeeded":
        messages.error(request, "Payment was not successful.")
        return redirect("cart_summary")

    # -------------------------------------------------
    # GET CUSTOMER INFORMATION
    # -------------------------------------------------

    email = None
    full_name = "Guest Customer"
    shipping_address = "Saved during checkout"

    # Logged-in customer
    if request.user.is_authenticated:

        shipping_addr = ShippingAddress.objects.filter(
            user=request.user
        ).first()

        if shipping_addr:

            if shipping_addr.shipping_email:
                email = shipping_addr.shipping_email

            if hasattr(shipping_addr, "shipping_full_name"):
                if shipping_addr.shipping_full_name:
                    full_name = shipping_addr.shipping_full_name

        # Fall back to account email
        if not email:
            email = request.user.email

        # Fall back to username/name
        if request.user.get_full_name():
            full_name = request.user.get_full_name()
        elif request.user.username:
            full_name = request.user.username

    # Guest customer
    else:

        # Try to obtain the email from Stripe
        if intent.receipt_email:
            email = intent.receipt_email

        # Try Stripe customer details if available
        if not email and getattr(intent, "customer", None):

            try:
                customer = stripe.Customer.retrieve(intent.customer)

                if customer.email:
                    email = customer.email

                if customer.name:
                    full_name = customer.name

            except stripe.error.StripeError:
                pass

    # Final fallback
    if not email:
        email = "customer@kentehaven.com"

    # -------------------------------------------------
    # CREATE ORDER
    # -------------------------------------------------

    order = Order.objects.create(

        user=(
            request.user
            if request.user.is_authenticated
            else None
        ),

        full_name=full_name,

        email=email,

        shipping_address=shipping_address,

        total_price=cart.get_total(),

        stripe_pid=payment_intent,

        paid=True
    )

    # -------------------------------------------------
    # CREATE ORDER ITEMS
    # -------------------------------------------------

    for product_id, item in cart.cart.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        quantity = int(item["quantity"])

        # Check stock before reducing it
        if product.stock < quantity:

            messages.error(
                request,
                f"{product.name} is out of stock."
            )

            # Remove the incomplete order
            order.delete()

            return redirect("cart_summary")

        # Reduce stock
        product.stock -= quantity
        product.save()

        # Determine the actual price paid
        if product.is_sale:
            price_paid = product.sale_price
        else:
            price_paid = product.price

        # Create order item
        OrderItem.objects.create(

            order=order,

            product=product,

            user=(
                request.user
                if request.user.is_authenticated
                else None
            ),

            quantity=quantity,

            price=product.price,

            price_paid=price_paid
        )

    # -------------------------------------------------
    # CLEAR CART
    # -------------------------------------------------

    cart.clear()

    # -------------------------------------------------
    # SEND CONFIRMATION EMAIL
    # -------------------------------------------------

    messages.success(
        request,
        "Payment successful! Your order has been placed."
    )

    send_mail(

        subject="Order Confirmation – Kente Haven",

        message=(
            f"Thank you for your order #{order.id}.\n\n"
            f"Total: £{order.total_price}\n\n"
            "We will process your order shortly."
        ),

        from_email=settings.DEFAULT_FROM_EMAIL,

        recipient_list=[order.email],

        fail_silently=True,
    )

    # -------------------------------------------------
    # DISPLAY SUCCESS PAGE
    # -------------------------------------------------

    return render(
        request,
        "payment/payment_success.html",
        {
            "order": order
        }
    )

# @login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        
    )

    return render(
        request,
        "payment/order_detail.html",
        {
            "order": order,
        }
    )

# @login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "payment/order_history.html", {"orders": orders})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = json.loads(payload)
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)


    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        Order.objects.filter(stripe_pid=intent["id"]).update(paid=True)

    return HttpResponse(status=200)
