from django.contrib import admin
from .models import (
    Product,
    Category,
    SubCategory,
    Order,
    OrderItem,
    Customer,
    Wishlist,
    ProductImage,
)
from .utils import generate_product_description


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ("title", "price", "sale_price", "is_on_sale")
    list_filter = ("sale_price",)

    def save_model(self, request, obj, form, change):
        if not obj.description:
            obj.description = generate_product_description(obj.title)
        super().save_model(request, obj, form, change)


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
