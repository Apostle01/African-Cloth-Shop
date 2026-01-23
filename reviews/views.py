from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product
from payment.models import OrderItem
from .models import ProductReview


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # ✅ PLACE THE SNIPPET HERE (RIGHT HERE)
    has_bought = OrderItem.objects.filter(
        user=request.user,
        product=product,
        order__paid=True
    ).exists()

    if not has_bought:
        messages.error(
            request,
            "You can only review products you have purchased."
        )
        return redirect("product_detail", product.id)

    # ----------------------------------
    # Continue normal review flow
    # ----------------------------------

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        ProductReview.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                "rating": rating,
                "comment": comment,
            }
        )

        messages.success(request, "Thank you for your review!")
        return redirect("product_detail", product.id)

    return render(request, "reviews/add_review.html", {
        "product": product
    })
