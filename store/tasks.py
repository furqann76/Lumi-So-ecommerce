from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from store.models import Order


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
