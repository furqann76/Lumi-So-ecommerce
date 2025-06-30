from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_order_confirmation_email(email, order_id):
    subject = f"Order Confirmation - #{order_id}"
    message = f"Thank you for your order #{order_id}! We are processing it."
    send_mail(
        subject,
        message,
        "no-reply@lumi-ecommerce.com",
        [email],
        fail_silently=False,
    )
