from django.shortcuts import render, get_object_or_404
from ..models import Order, OrderItem
from store.tasks import send_order_confirmation_email


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)

    # Trigger the email task
    send_order_confirmation_email.delay(request.user.email, order.id)

    return render(request, "store/order_success.html", {"order": order})
