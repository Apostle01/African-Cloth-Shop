from django.core.mail import send_mail
from django.conf import settings


def send_order_status_email(order):
    subject_map = {
        "shipped": "Your order has been shipped 🚚",
        "delivered": "Your order has been delivered 📦",
    }

    message_map = {
        "shipped": f"""
Hi,

Good news! Your order #{order.id} has been shipped.

It’s on the way to you 🚚

Thank you for shopping with us.
""",
        "delivered": f"""
Hi,

Your order #{order.id} has been successfully delivered 📦

We hope you enjoy your purchase.
Thank you for shopping with us!
""",
    }

    status = order.status

    if status in subject_map:
        send_mail(
            subject_map[status],
            message_map[status],
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            fail_silently=False,
        )
