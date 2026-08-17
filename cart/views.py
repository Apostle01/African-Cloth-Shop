from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest

from .cart import Cart
from products.models import Product

def cart_summary(request):
    cart = Cart(request)

    items = []
    for key, value in cart.cart.items():
        product_id = int(key)  
        product = get_object_or_404(Product, id=product_id)

        quantity = int(value.get("quantity", 1))
        price = float(product.current_price)
        subtotal = price * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal,
        })

    context = {
        "cart_items": items,
        "cart_total": cart.get_total(),
    }
    return render(request, "cart/cart_summary.html", context)

# def cart_add(request):
#     print("REQUEST METHOD:", request.method)
#     print("POST DATA:", request.POST)

#     if request.method == "POST":
#         return HttpResponseBadRequest("Invalid request method")

#     product_id = request.POST.get("product_id")
#     quantity = request.POST.get("quantity", 1)

#     if not product_id:
#         return HttpResponseBadRequest("Product ID is required")

#     try:
#         product_id = int(product_id)
#         quantity = int(quantity)
#     except (TypeError, ValueError):
#         return HttpResponseBadRequest("Invalid product ID or quantity")

#     if quantity < 1:
#         return HttpResponseBadRequest("Quantity must be at least 1")

#     product = get_object_or_404(Product, id=int(product_id))
        
#     cart = Cart(request)
#     cart.add(product, quantity=quantity)
        
#     return redirect("cart_summary")
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
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity")

    if not product_id or not quantity:
        return HttpResponseBadRequest("Invalid data")

    try:
        product_id = int(product_id)
        quantity = int(quantity)
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid product ID or quantity")

    if quantity < 1:
        return HttpResponseBadRequest("Quantity must be at least 1")

    product = get_object_or_404(Product, id=product_id)

    cart = Cart(request)
    cart.update(product, quantity)

    return redirect("cart_summary")

def cart_delete(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    product_id = request.POST.get("product_id")

    if not product_id:
        return HttpResponseBadRequest("Product ID is required")

    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid product ID")

    product = get_object_or_404(Product, id=product_id)

    cart = Cart(request)
    cart.delete(product)

    return redirect("cart_summary")

def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("cart_summary")

    items = []

    for key, value in cart.cart.items():
        product_id = int(key)
        product = get_object_or_404(Product, id=product_id)

        quantity = value.get("quantity", 1)
        price = float(product.current_price)
        subtotal = price * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal,
        })

    return render(request, "checkout.html", {
        "cart_items": items,
        "cart_total": cart.get_total(),
    })

