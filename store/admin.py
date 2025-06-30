from django.contrib import admin, messages
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
from .models.theme import SiteTheme


@admin.action(description="Activate selected theme (only one at a time)")
def activate_theme(modeladmin, request, queryset):
    if queryset.count() != 1:
        messages.error(request, "Please select exactly one theme to activate.")
        return

    # Deactivate all themes first
    SiteTheme.objects.update(is_active=False)

    # Activate selected theme
    selected = queryset.first()
    selected.is_active = True
    selected.save()

    messages.success(request, f"'{selected.name}' theme has been activated.")


@admin.register(SiteTheme)
class SiteThemeAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "updated_at"]
    actions = [activate_theme]


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
