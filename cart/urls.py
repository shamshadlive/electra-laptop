from django.urls import path

from . import views

urlpatterns = [
    path("", views.cart, name="cart"),
    path("add_cart/<int:product_id>/", views.add_cart, name="add-cart"),
    path("remove_cart/<int:product_id>/", views.remove_cart, name="remove-cart"),
    path("remove_cart_item/<int:product_id>/", views.remove_cart_item, name="remove-cart-item"),
    path("checkout/", views.checkout, name="checkout"),
    
    path("checkout/coupon/verify", views.coupon_verify, name="coupon_verify"),
    
    
    path("whishlist/add/", views.add_whishlist, name="add_whishlist"),
    
]