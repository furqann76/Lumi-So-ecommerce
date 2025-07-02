from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from store.models import Order
from django.utils import timezone
from datetime import timedelta
from .models.abandoned_cart import AbandonedCart
from django.core.mail import send_mail


@shared_task
def send_order_confirmation_email(email, order_id):
    from store.models import Order  # Ensure this import is correct

    try:
        order = Order.objects.get(id=order_id)

        subject = f"Order #{order.id} Confirmation - Lumi & So"
        message = render_to_string(
            "emails/order_confirmation.html",
            {
                "customer_name": order.user.get_full_name(),
                "order_number": order.id,
                "order_date": order.order_date.strftime("%B %d, %Y"),
                "payment_method": order.payment_method,
                "shipping_address": order.shipping_address,
                "order_items": order.items.all(),  # if you relate items to orders
                "subtotal": order.subtotal,
                "shipping_fee": order.shipping_fee,
                "total_amount": order.total_amount,
                "order_tracking_link": f"https://127.0.0.1:8000/orders/{order.id}/",
            },
        )

        email_message = EmailMessage(
            subject, message, "no-reply@lumi-ecommerce.com", [email]
        )
        email_message.content_subtype = "html"
        email_message.send()

    except Order.DoesNotExist:
        print(f"Order with ID {order_id} does not exist.")


@shared_task
def send_cart_recovery_emails():
    threshold = timezone.now() - timedelta(minutes=4)
    carts = AbandonedCart.objects.filter(emailed=False, created_at__lte=threshold)

    for cart in carts:
        subject = "You left items in your cart"
        message = render_to_string(
            "emails/cart_recovery.html",
            {
                "customer_name": cart.user.first_name or cart.user.username,
                "cart_data": cart.cart_data,
            },
        )
        send_mail(
            subject, "", "yourshop@example.com", [cart.user.email], html_message=message
        )
        cart.emailed = True
        cart.save()
