from django.db import models


class CompetitorProduct(models.Model):
    name = models.CharField(max_length=255)
    your_product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    competitor_url = models.URLField()
    latest_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} for {self.your_product.name}"
