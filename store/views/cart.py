from django.shortcuts import redirect, render
from ..cart import Cart


def add_to_cart(request, product_id):
    cart = Cart(request)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        selected_size = request.POST.get("selected_size")
        cart.add(product_id, quantity=quantity, size=selected_size)
    else:
        cart.add(product_id)
    return redirect("cart")


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect("cart")


def cart_view(request):
    cart = Cart(request)
    return render(request, "store/cart.html", {"cart": cart})


def increase_quantity(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect("cart")


def decrease_quantity(request, product_id):
    cart = Cart(request)
    cart.decrease(product_id)
    return redirect("cart")


def place_order(request):
    if request.user.is_authenticated:
        user = request.user
