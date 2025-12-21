import stripe
from django.contrib import admin
from django.db.models import Sum
from django.conf import settings
from .models import ShippingAddress, Order, OrderItem

from .models import Order

admin.site.register(ShippingAddress)

@admin.action(description="Refund selected orders")
def refund_orders(modeladmin, request, queryset):
    stripe.api_key = settings.STRIPE_SECRET_KEY

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


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price")