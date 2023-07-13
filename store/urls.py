from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    
    path("store/", views.store, name="store"),
    path("store/<slug:category_slug>/", views.store, name="product-by-category"),
    path("store/<slug:category_slug>/<slug:product_variant_slug>", views.product_variant_detail, name="product-variant-detail"),
    
    # USER DASHBOARD 
    path("user/dashboard", views.user_dashboard, name="user-dashboard"),
    path("user/order_history", views.order_history, name="order-history"),
    path("user/order_history/<str:order_id>", views.order_history_detail, name="order-history-detail"),
    
    #ADRESS USER
    path("user/address", views.user_address, name="user-address"),
    path("user/address/create/<str:checkout>", views.user_address_create, name="user-address-create"),
    path("user/address/make_default/<str:adress_id>", views.user_address_make_default, name="user-address-make-default"),
    path("user/address/delete/<str:adress_id>", views.user_address_delete, name="user-address-delete"),
    
    
]