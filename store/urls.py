from django.urls import path

from . import views
from offer_management import views as offer_management_views
urlpatterns = [
    path("", views.home, name="home"),
    
    
    #autocomplete
    path("autocomplete", views.autocomplete, name="autocomplete"),
    
    
    
    path("store/", views.store, name="store"),
    path("store/<slug:category_slug>/", views.store, name="product-by-category"),
    path("store/<slug:category_slug>/<slug:product_variant_slug>", views.product_variant_detail, name="product-variant-detail"),
    
    # USER DASHBOARD 
    path("user/dashboard", views.user_dashboard, name="user-dashboard"),
    path("user/order_history", views.order_history, name="order-history"),
    path("user/order_history/<str:order_id>", views.order_history_detail, name="order-history-detail"),
    path("user/wishlist", views.user_wishlist, name="user-wishlist"),
    
    #ADRESS USER
    path("user/address", views.user_address, name="user-address"),
    path("user/address/create/<str:checkout>", views.user_address_create, name="user-address-create"),
    path("user/address/make_default/<str:adress_id>", views.user_address_make_default, name="user-address-make-default"),
    path("user/address/delete/<str:adress_id>", views.user_address_delete, name="user-address-delete"),

    #store offers
    path("store/offers", offer_management_views.all_offers_store.as_view(), name="store-all-offers"),
    path("store/offers/category/<str:offer_slug>", offer_management_views.category_offer_product.as_view(), name="store-category-offers"),
    path("store/offers/category/<str:offer_slug>/<str:category>", offer_management_views.category_offer_product.as_view(), name="store-category-offers-each"),
    
    path("store/offers/product/<str:offer_slug>", offer_management_views.product_offer_product.as_view(), name="store-product-offers"),
    
    
    #submit review
    path("submit_review/<int:product_id>/", views.submit_review, name="submit_review"),
    
    
    
]