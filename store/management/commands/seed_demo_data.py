"""
Populate the database with sample storefront data: categories, subcategories,
products (with gallery images and a couple of on-sale / out-of-stock cases),
demo customers, a sample order, reviews, and an active site theme.

Safe to re-run: everything is looked up by a natural key first, so running
this command again will not create duplicates.

Usage:
    python manage.py seed_demo_data
    python manage.py seed_demo_data --flush   # wipe existing demo data first
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from store.models import (
    Category,
    SubCategory,
    Product,
    ProductImage,
    Order,
    OrderItem,
    Customer,
    Wishlist,
)
from store.models.product import Review
from store.models.theme import SiteTheme

# (title, price, sale_price, stock, available_sizes, image, gallery_images, description)
PRODUCTS_BY_SUBCATEGORY = {
    ("Men", "Shirts"): [
        (
            "Classic White Oxford Shirt",
            "45.00", None, 20, ["S", "M", "L", "XL"],
            "products/shirt.webp", [],
            "A crisp, tailored oxford shirt in classic white — breathable cotton "
            "that works equally well tucked into chinos or dressed down with denim.",
        ),
        (
            "Slim Fit Blue Check Shirt",
            "49.99", "39.99", 15, ["S", "M", "L"],
            "products/shirt_7AMpzLD.webp", [],
            "A slim-fit checked shirt with a soft brushed finish, cut for a "
            "modern silhouette without feeling restrictive.",
        ),
        (
            "Casual Linen Shirt",
            "55.00", None, 0, ["M", "L", "XL"],
            "products/shirt_8LGmDmz.webp", [],
            "Lightweight linen-blend shirt built for warm days — relaxed fit, "
            "breathable weave, effortlessly casual.",
        ),
    ],
    ("Men", "Denim"): [
        (
            "Straight Fit Denim Jeans",
            "65.00", None, 30, ["S", "M", "L", "XL"],
            "products/denim.webp", ["products/gallery/denim.webp"],
            "Durable straight-fit denim with just enough stretch for all-day "
            "comfort. A wardrobe staple that pairs with anything.",
        ),
        (
            "Vintage Wash Denim Jacket",
            "89.99", "74.99", 10, ["M", "L", "XL"],
            "products/denim_LQCRzOO.webp", [],
            "A vintage-wash denim jacket with a broken-in feel from day one — "
            "layer it over tees or hoodies for an easy street-ready look.",
        ),
    ],
    ("Men", "Cargo Pants"): [
        (
            "Utility Cargo Pants",
            "59.99", None, 25, ["S", "M", "L", "XL"],
            "products/cargo1.webp", ["products/gallery/cargo1.webp"],
            "Six-pocket utility cargo pants in a durable cotton twill, built "
            "for function without giving up a clean silhouette.",
        ),
        (
            "Relaxed Fit Cargo Shorts",
            "39.99", None, 18, ["S", "M", "L"],
            "products/cargo1_7LwxBsd.webp", [],
            "Relaxed cargo shorts with reinforced stitching and deep side "
            "pockets — built for warm-weather wear.",
        ),
    ],
    ("Women", "Tops"): [
        (
            "Silk Blend Camisole Top",
            "42.00", None, 22, ["XS", "S", "M", "L"],
            "products/shirt2.webp", ["products/gallery/shirt2.webp"],
            "A fluid silk-blend camisole with adjustable straps — dress it up "
            "with a blazer or wear it on its own.",
        ),
        (
            "Ruffle Sleeve Blouse",
            "48.50", "36.00", 12, ["S", "M", "L"],
            "products/shirt2_O9iU8mM.webp", [],
            "A lightweight blouse with soft ruffle-sleeve detailing, cut for "
            "an easy drape that moves with you.",
        ),
    ],
    ("Women", "Dresses"): [
        (
            "Floral Wrap Midi Dress",
            "78.00", None, 8, ["XS", "S", "M", "L"],
            "products/shirt2.webp", [],
            "A wrap-style midi dress in a soft floral print, finished with a "
            "tie waist for a flattering, adjustable fit.",
        ),
        (
            "Little Black Dress",
            "95.00", "79.00", 5, ["S", "M", "L"],
            "products/shirt_qGCG9XQ.webp", [],
            "An effortless black dress cut for evenings out — a fitted "
            "silhouette in a comfortable stretch fabric.",
        ),
    ],
    ("Accessories", "Bags"): [
        (
            "Leather Tote Bag",
            "120.00", None, 10, ["One Size"],
            "products/cargo1_ZYcmYkW.webp", [],
            "A structured leather tote with an interior zip pocket and "
            "magnetic closure — roomy enough for daily essentials.",
        ),
        (
            "Canvas Crossbody Bag",
            "45.00", None, 0, ["One Size"],
            "products/denim.webp", [],
            "A compact canvas crossbody with an adjustable strap, built for "
            "everyday carry.",
        ),
    ],
    ("Accessories", "Jewelry"): [
        (
            "Minimalist Gold Necklace",
            "35.00", None, 40, ["One Size"],
            "products/shirt_O63YZKb.webp", [],
            "A delicate gold-plated chain necklace with a minimalist pendant "
            "— easy to layer or wear on its own.",
        ),
        (
            "Silver Hoop Earrings",
            "28.00", "22.00", 33, ["One Size"],
            "products/shirt_W0vnNcr.webp", [],
            "Classic sterling silver hoops, lightweight enough for everyday "
            "wear.",
        ),
    ],
}

DEMO_CUSTOMERS = [
    dict(
        username="jane_doe",
        email="jane.doe@example.com",
        first_name="Jane",
        last_name="Doe",
        password="demopass123",
        phone_number="+1 555-0100",
        shipping_address="221B Baker Street, Springfield, IL 62701",
        billing_address="221B Baker Street, Springfield, IL 62701",
        date_of_birth="1994-03-12",
    ),
    dict(
        username="john_smith",
        email="john.smith@example.com",
        first_name="John",
        last_name="Smith",
        password="demopass123",
        phone_number="+1 555-0101",
        shipping_address="742 Evergreen Terrace, Springfield, IL 62704",
        billing_address="",
        date_of_birth="1990-07-25",
    ),
]

REVIEWS = [
    # (product title, username, rating, comment, sentiment)
    ("Classic White Oxford Shirt", "jane_doe", 5,
     "Great fit and the fabric feels premium. Runs true to size.", "Positive"),
    ("Straight Fit Denim Jeans", "john_smith", 4,
     "Comfortable and durable, exactly what I needed for daily wear.", "Positive"),
    ("Casual Linen Shirt", "jane_doe", 2,
     "Wish it wasn't out of stock in my size for so long.", "Negative"),
    ("Ruffle Sleeve Blouse", "john_smith", 5,
     "Bought this for my wife, she loves it.", "Positive"),
    ("Utility Cargo Pants", "jane_doe", 3,
     "Good pants, pockets are a bit shallow.", "Neutral"),
]


class Command(BaseCommand):
    help = "Seed the database with sample storefront data (categories, products, customers, orders, reviews)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing demo products/categories/customers/orders/reviews before reseeding.",
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            if options["flush"]:
                self._flush()
            self._seed_theme()
            self._seed_categories_and_products()
            customers = self._seed_customers()
            self._seed_reviews()
            self._seed_order(customers["jane_doe"])
            self._seed_wishlist(customers["john_smith"])

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))

    def _flush(self):
        self.stdout.write("Flushing existing demo data...")
        Review.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Wishlist.objects.all().delete()
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        SubCategory.objects.all().delete()
        Category.objects.all().delete()
        Customer.objects.filter(user__username__in=[c["username"] for c in DEMO_CUSTOMERS]).delete()
        User.objects.filter(username__in=[c["username"] for c in DEMO_CUSTOMERS]).delete()

    def _seed_theme(self):
        for name in ("light", "dark", "custom"):
            SiteTheme.objects.get_or_create(name=name)
        SiteTheme.objects.update(is_active=False)
        SiteTheme.objects.filter(name="light").update(is_active=True)
        self.stdout.write("Themes ready ('light' active).")

    def _seed_categories_and_products(self):
        created_products = 0
        for (category_name, subcategory_name), products in PRODUCTS_BY_SUBCATEGORY.items():
            category, _ = Category.objects.get_or_create(name=category_name)
            subcategory, _ = SubCategory.objects.get_or_create(
                category=category, name=subcategory_name
            )
            for title, price, sale_price, stock, sizes, image, gallery, description in products:
                product, was_created = Product.objects.get_or_create(
                    title=title,
                    defaults=dict(
                        description=description,
                        price=Decimal(price),
                        sale_price=Decimal(sale_price) if sale_price else None,
                        subcategory=subcategory,
                        available_sizes=sizes,
                        stock=stock,
                        image=image,
                    ),
                )
                if was_created:
                    created_products += 1
                    for gallery_image in gallery:
                        ProductImage.objects.create(product=product, image=gallery_image)
        self.stdout.write(f"Products ready ({created_products} created).")

    def _seed_customers(self):
        customers = {}
        for data in DEMO_CUSTOMERS:
            user, was_created = User.objects.get_or_create(
                username=data["username"],
                defaults=dict(email=data["email"], first_name=data["first_name"], last_name=data["last_name"]),
            )
            if was_created:
                user.set_password(data["password"])
                user.save()
            Customer.objects.get_or_create(
                user=user,
                defaults=dict(
                    phone_number=data["phone_number"],
                    shipping_address=data["shipping_address"],
                    billing_address=data["billing_address"],
                    date_of_birth=data["date_of_birth"] or None,
                ),
            )
            customers[data["username"]] = user
        self.stdout.write(f"Demo customers ready ({', '.join(customers)}) — password: demopass123")
        return customers

    def _seed_reviews(self):
        created = 0
        for title, username, rating, comment, sentiment in REVIEWS:
            try:
                product = Product.objects.get(title=title)
                user = User.objects.get(username=username)
            except (Product.DoesNotExist, User.DoesNotExist):
                continue
            _, was_created = Review.objects.get_or_create(
                product=product,
                user=user,
                defaults=dict(rating=rating, comment=comment, sentiment=sentiment),
            )
            created += was_created
        self.stdout.write(f"Reviews ready ({created} created).")

    def _seed_order(self, user):
        if Order.objects.filter(user=user).exists():
            self.stdout.write("Sample order already exists, skipping.")
            return
        items = [
            ("Classic White Oxford Shirt", 1),
            ("Straight Fit Denim Jeans", 2),
        ]
        subtotal = Decimal("0.00")
        line_items = []
        for title, quantity in items:
            product = Product.objects.get(title=title)
            subtotal += product.get_display_price() * quantity
            line_items.append((product, quantity))

        shipping_fee = Decimal("5.00")
        order = Order.objects.create(
            user=user,
            name=user.get_full_name() or user.username,
            address=user.customer.shipping_address,
            phone=user.customer.phone_number,
            payment_method="COD",
            shipping_address=user.customer.shipping_address,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            total_amount=subtotal + shipping_fee,
        )
        for product, quantity in line_items:
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        self.stdout.write(f"Sample order #{order.id} created for {user.username}.")

    def _seed_wishlist(self, user):
        for title in ("Little Black Dress", "Leather Tote Bag"):
            product = Product.objects.get(title=title)
            Wishlist.objects.get_or_create(user=user, product=product)
        self.stdout.write(f"Wishlist ready for {user.username}.")
