from django.db import models
from .category import SubCategory
from django.contrib.auth.models import User


class Product(models.Model):
    SIZES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "X-Large"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    available_sizes = models.JSONField(default=list)
    stock = models.PositiveIntegerField(default=10)  # 👈 Add this line

    def is_in_stock(self):
        return self.stock > 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        return f"{self.product.title} - Extra Image"


class Review(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    sentiment = models.CharField(
        max_length=10,
        choices=[
            ("Positive", "Positive"),
            ("Negative", "Negative"),
            ("Neutral", "Neutral"),
        ],
        default="Neutral",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} ({self.rating})"
