from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", views.register_view, name="register"),
    path("", views.home, name="home"),
    path("profile/", views.profile_view, name="profile"),
    path("search/", views.search_products, name="search_products"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path(
        "wishlist/add/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"
    ),
    path(
        "wishlist/remove/<int:product_id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist",
    ),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "remove-from-cart/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path(
        "cart/increase/<int:product_id>/",
        views.increase_quantity,
        name="increase_quantity",
    ),
    path(
        "cart/decrease/<int:product_id>/",
        views.decrease_quantity,
        name="decrease_quantity",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
    path(
        "subcategory/<int:subcategory_id>/",
        views.subcategory_products,
        name="subcategory_products",
    ),
]
