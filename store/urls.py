from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("store", views.store, name="store"),
    path("store/<slug:category_slug>", views.store, name="product-by-category"),
    path("store/<slug:category_slug>/<slug:product_variant_slug>", views.product_variant_detail, name="product-variant-detail"),
    
    
    
]