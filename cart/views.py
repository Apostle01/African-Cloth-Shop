from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from products.models import Product
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    return render(request, "cart_summary.html", {"cart": cart})


def cart_add(request):
    # Get the cart object
    cart = Cart(request)

    if request.method == "POST":
        product_id = request.POST.get("product_id")

        if not product_id:
            return JsonResponse({"success": False, "error": "Missing product id"}, status=400)

        product = get_object_or_404(Product, id=product_id)

        quantity = int(request.POST.get("quantity", 1))
        cart.add(product=product, quantity=quantity)


        return JsonResponse({
            "success": True,
            "product": product.name,
            "cart_total": len(cart),
        })

        return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def cart_delete(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        cart = Cart(request)
        cart.remove(product)

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)

def cart_update(request):
    pass


