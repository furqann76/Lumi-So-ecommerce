from django.shortcuts import render, get_object_or_404, redirect
from ..models import Product, SubCategory
from ..utils import get_ai_related_products
from ..models import Product
from ..forms import ReviewForm
from django.contrib import messages
from ..models.product import Review
from django.db.models import Q
from django.core.paginator import Paginator
from textblob import TextBlob


def search_products(request):
    query = request.GET.get("q", "")
    products = Product.objects.filter(Q(title__icontains=query)) if query else []

    return render(
        request,
        "store/search_results.html",
        {
            "query": query,
            "products": products,
        },
    )


def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})


def subcategory_products(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    products = Product.objects.filter(subcategory=subcategory)

    # --- Filters ---
    availability = request.GET.getlist("availability")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort")

    if "in" in availability:
        products = products.filter(stock__gt=0)
    if "out" in availability:
        products = products.filter(stock__lte=0)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # --- Sorting ---
    if sort == "newest":
        products = products.order_by("-id")
    elif sort == "low":
        products = products.order_by("price")
    elif sort == "high":
        products = products.order_by("-price")

    # --- Pagination ---
    paginator = Paginator(products, 6)  # Show 6 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "subcategory": subcategory,
        "page_obj": page_obj,
        "min_price": min_price or 0,
        "max_price": max_price or 10000,
        "selected_availability": availability,
        "selected_sort": sort,
    }

    return render(request, "store/subcategory_products.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    related_products = get_ai_related_products(product)
    reviews = product.reviews.all().order_by("-created_at")
    review_form = ReviewForm()

    # -------------------------------
    # Recently Viewed Logic
    recently_viewed = request.session.get("recently_viewed", [])

    if product_id in recently_viewed:
        recently_viewed.remove(product_id)  # Remove and re-add to move it to top

    recently_viewed.insert(0, product_id)  # Add to beginning
    recently_viewed = recently_viewed[:5]  # Limit to last 5

    request.session["recently_viewed"] = recently_viewed

    recently_viewed_products = Product.objects.filter(id__in=recently_viewed).exclude(
        id=product_id
    )
    # -------------------------------

    if request.method == "POST" and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user

            # --- Sentiment Analysis ---
            comment_text = review.comment
            analysis = TextBlob(comment_text)
            polarity = analysis.sentiment.polarity

            if polarity >= 3:
                review.sentiment = "Positive"
            elif polarity <= 2:
                review.sentiment = "Negative"
            else:
                review.sentiment = "Neutral"
            # --------------------------

            review.save()
            messages.success(request, "Your review has been submitted.")
            return redirect("product_detail", product_id=product_id)

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
            "reviews": reviews,
            "review_form": review_form,
            "recently_viewed_products": recently_viewed_products,
        },
    )
