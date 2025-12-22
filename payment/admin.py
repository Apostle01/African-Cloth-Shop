from django.contrib import admin
from django.db.models import Sum
from django.conf import settings
from django.core.mail import send_mail
import stripe

from .models import Order, OrderItem, ShippingAddress

stripe.api_key = settings.STRIPE_SECRET_KEY


@admin.action(description="Refund selected orders")
def refund_orders(modeladmin, request, queryset):
    for order in queryset.filter(paid=True):
        if order.stripe_pid:
            stripe.Refund.create(payment_intent=order.stripe_pid)
            order.paid = False
            order.save()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email", "total_price", "paid", "status", "created")
    list_filter = ("paid", "status", "created")
    search_fields = ("email", "stripe_pid")
    ordering = ("-created",)
    actions = [refund_orders]

    def save_model(self, request, obj, form, change):
        if change:
            old_status = Order.objects.get(pk=obj.pk).status
            if old_status != obj.status:
                send_mail(
                    subject=f"Your order #{obj.id} is now {obj.get_status_display()}",
                    message=(
                        f"Hello,\n\n"
                        f"Your order #{obj.id} status has changed to "
                        f"{obj.get_status_display()}.\n\n"
                        f"Thank you for shopping with us!"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.email],
                    fail_silently=True,
                )
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            qs = response.context_data["cl"].queryset
            revenue = qs.filter(paid=True).aggregate(
                total=Sum("total_price")
            )["total"] or 0
            response.context_data["total_revenue"] = revenue
        except Exception:
            pass
        return response


admin.site.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price")
    
admin.site.register(ShippingAddress)
