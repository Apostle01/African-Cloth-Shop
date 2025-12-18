import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cart.cart import Cart
from .models import Order, OrderItem, ShippingAddress
from .forms import ShippingForm
from products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart_summary")

    # Load existing shipping address if it exists
    shipping_address = ShippingAddress.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = ShippingForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = request.user
            shipping.save()

            return redirect("payment:payment")
    else:
        form = ShippingForm(instance=shipping_address)

    context = {
        'form': form,
        'cart_items': cart,
        'cart_total': cart.get_total(),
    }

    return render(request, "payment/checkout.html", context)


@login_required
def payment(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, "Your cart is empty")
        return redirect("cart_summary")

    amount = int(cart.get_total() * 100)  # Stripe uses cents

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency="usd",
        automatic_payment_methods={"enabled": True},
        metadata={"user_id": request.user.id}
    )

    return render(request, "payment/payment.html", {
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "client_secret": intent.client_secret,
        "site_url": settings.SITE_URL,
        "cart": cart,
        "total": cart.get_total(),
        "site_url": settings.SITE_URL,  
    })

@login_required
def payment_success(request):
    cart = Cart(request)

    payment_intent = request.GET.get("payment_intent")

    if not payment_intent:
        messages.error(request, "Payment not verified.")
        return redirect("payment:payment")

    intent = stripe.PaymentIntent.retrieve(payment_intent)

    if intent.status != "succeeded":
        messages.error(request, "Payment failed.")
        return redirect("payment:payment")

    order = Order.objects.create(
        user=request.user,
        total_price=cart.get_total(),
        paid=True,
        stripe_pid=intent.id
    )

    for product_id, item in cart.cart.items():
        product = get_object_or_404(Product, id=product_id)
        OrderItem.objects.create(
            order=order,
            product=product,
            price=item['price'],
            quantity=item['quantity']
        )

    cart.clear()
    messages.success(request, "Payment successful!")

    return redirect('products:all_products')
