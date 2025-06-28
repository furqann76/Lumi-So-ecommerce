from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from ..models import Order, OrderItem


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)

    # Send order confirmation email
    subject = "Order Confirmation - Lumi & So"
    message = f"Hi {order.user.username},\n\nYour order #{order.id} has been successfully placed. Thank you for shopping with us!"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=False,
    )

    return render(request, "store/order_success.html", {"order": order, "items": items})
