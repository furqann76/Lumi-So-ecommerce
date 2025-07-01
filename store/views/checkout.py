# store/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from ..cart import Cart
from ..forms.checkout import CheckoutForm
from ..models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart(request)
    subtotal = sum(item["product"].price * item["quantity"] for item in cart)
    shipping_fee = 200  # flat shipping fee
    total_amount = subtotal + shipping_fee

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                name=form.cleaned_data.get("name"),
                address=form.cleaned_data.get("address"),
                phone=form.cleaned_data.get("phone"),
                shipping_address=form.cleaned_data.get("address"),
                payment_method=form.cleaned_data.get("payment_method"),
                order_date=timezone.now(),
                subtotal=subtotal,
                shipping_fee=shipping_fee,
                total_amount=total_amount,
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item["product"], quantity=item["quantity"]
                )

            # Optional: update customer profile
            try:
                customer = request.user.customer
                customer.shipping_address = form.cleaned_data["address"]
                customer.phone_number = form.cleaned_data["phone"]
                customer.save()
            except:
                pass  # ignore if profile doesn't exist

            # Clear cart
            cart.clear()

            messages.success(request, "Order placed successfully!")
            return redirect("order_success", order_id=order.id)
    else:
        form = CheckoutForm()

    return render(
        request,
        "store/checkout.html",
        {
            "form": form,
            "cart": cart,
            "subtotal": subtotal,
            "shipping_fee": shipping_fee,
            "total_amount": total_amount,
        },
    )
