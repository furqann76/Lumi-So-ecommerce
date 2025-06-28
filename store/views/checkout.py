from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..cart import Cart
from ..forms.checkout import CheckoutForm
from ..models import Order, OrderItem
from django.contrib import messages


@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                name=form.cleaned_data["name"],
                address=form.cleaned_data["address"],
                phone=form.cleaned_data["phone"],
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item["product"], quantity=item["quantity"]
                )

            # Update customer profile if exists
            try:
                customer = request.user.customer
                customer.shipping_address = form.cleaned_data["address"]
                customer.phone_number = form.cleaned_data["phone"]
                customer.save()
            except:
                pass  # If customer profile does not exist, ignore silently

            cart.clear()
            messages.success(request, "Order placed successfully!")
            return redirect("order_success", order_id=order.id)
    else:
        form = CheckoutForm()
    return render(request, "store/checkout.html", {"form": form, "cart": cart})
