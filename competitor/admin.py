from django.contrib import admin
from .models import CompetitorProduct


@admin.register(CompetitorProduct)
class CompetitorProductAdmin(admin.ModelAdmin):
    list_display = ("name", "your_product", "latest_price", "last_checked")
