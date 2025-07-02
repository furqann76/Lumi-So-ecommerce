from django.db import models
from django.contrib.auth.models import User


class AbandonedCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_data = models.JSONField(default=dict)  # ✅ VALID DEFAULT
    emailed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AbandonedCart for {self.user}"
