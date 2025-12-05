from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from products.models import Product
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)  # your cart class
    items = []

    for key, value in cart.cart.items():
        product = Product.objects.get(id=key)
        quantity = value['quantity']
        subtotal = product.price * quantity

        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': items,
        'cart_total': cart.get_total()
    }

    return render(request, 'cart_summary.html', context)


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
        if not product_id:
            return JsonResponse({"success": False, "error": "Missing product_id"}, status=400)
        
        product = get_object_or_404(Product, id=product_id)

        cart = Cart(request)
        cart.remove(product)

        return JsonResponse({"success": True, "message": "Item removed"})

    return JsonResponse({"success": False, "error": "Invalid method"}, status=400)



def cart_update(request):
    """
    Updates quantity of an item in the cart.
    """
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")

        if not product_id or not quantity:
            return JsonResponse({"success": False, "error": "Missing data"}, status=400)

        product = get_object_or_404(Product, id=product_id)

        cart = Cart(request)
        cart.update(product, quantity)

        return JsonResponse({"success": True, "message": "Quantity updated"})

    return JsonResponse({"success": False, "error": "Invalid method"}, status=400)


