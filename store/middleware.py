from .models.abandoned_cart import AbandonedCart


class AbandonedCartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ✅ Safe check before using request.user
        if hasattr(request, "user") and request.user.is_authenticated:
            cart = request.session.get("cart", {})
            if cart:
                AbandonedCart.objects.update_or_create(
                    user=request.user, emailed=False, defaults={"cart_data": cart}
                )

        return self.get_response(request)
