from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product
from payment.models import OrderItem
from .models import ProductReview
from .forms import ProductReviewForm


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

    # Prevent duplicate review
    if ProductReview.objects.filter(product=product, user=request.user).exists():
        messages.warning(request, "You have already reviewed this product")
        return redirect("product_detail", product.id)

    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review =form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Thank you for your review")
            return redirect("product_detail", product.id)

        else:
            form = ProductReviewForm()
        
        return render(request, "review/add_review.html", {
            "form": form,
            "product": product,
        })
        
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        ProductReview.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                "rating": request.POST["rating"],
                "comment": request.POST["comment"],
            }
        )

        messages.success(request, "Thank you for your review!")
        return redirect("product_detail", product.id)

    return render(request, "reviews/add_review.html", {
        "product": product
    })
