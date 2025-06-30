from .models import Category
from .models.theme import SiteTheme


def categories_processor(request):
    categories = Category.objects.prefetch_related("subcategories").all()
    return {"nav_categories": categories}


def current_theme(request):
    try:
        theme = SiteTheme.objects.get(is_active=True).name
    except SiteTheme.DoesNotExist:
        theme = "custom"
    return {"current_theme": theme}
