from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .cart import Cart
from django.urls import reverse
from products.models import Product


def cart_summary(request):
    cart = Cart(request)

    items = []
    for key, value in cart.cart.items():
        product_id = int(key)  # convert key from string to int
        product = get_object_or_404(Product, id=product_id)

        quantity = value.get("quantity", 1)
        price = float(value.get("price", product.price))
        subtotal = price * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    context = {
        "cart_items": items,
        "cart_total": cart.get_total(),
    }
    return render(request, "cart/cart_summary.html", context)

def cart_add(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        if not product_id:
            return redirect("cart_summary")
        product = get_object_or_404(Product, id=int(product_id))
        
        cart = Cart(request)
        cart.add(product)
        
    return redirect("cart_summary")

def cart_update(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")

        if not product_id or not quantity:
            return HttpResponseBadRequest("Invalid data")

        product = get_object_or_404(Product, id=product_id)

        cart = Cart(request)
        cart.update(product, int(quantity))

        return redirect("cart_summary")

    return HttpResponseBadRequest("Invalid request")


def cart_delete(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        if not product_id:
            return HttpResponseBadRequest("Invalid data")

        product = get_object_or_404(Product, id=product_id)
 
        cart = Cart(request)
        cart.delete(product)

        return redirect("cart_summary")

    return HttpResponseBadRequest("Invalid request")
