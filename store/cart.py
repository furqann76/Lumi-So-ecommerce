from decimal import Decimal
from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        # Ensure cart is a dict, not a list
        if not cart or not isinstance(cart, dict):
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product_id, quantity=1, size=None):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] += quantity
            if size:
                self.cart[product_id]["size"] = size
        else:
            self.cart[product_id] = {"quantity": quantity}
            if size:
                self.cart[product_id]["size"] = size
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["total_price"] = item["product"].price * item["quantity"]
            yield item

    def get_total_price(self):
        return sum(item["product"].price * item["quantity"] for item in self)

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def decrease(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] -= 1
            if self.cart[product_id]["quantity"] <= 0:
                self.remove(product_id)
            self.save()
