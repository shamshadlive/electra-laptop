from django.urls import path
from categoryManagement import views as categoryView
from product_management import views as productView
from extra_management import views as extraView
from order import views as orderView
from offer_management import views as offerView
from . import views

urlpatterns = [
    path("", views.admin_home, name="admin-home"),
    
    
    #chart data api
    path("api/dashboard/data/sales", views.DashboardSalesData.as_view(), name="api-dashboard-sales"),
    path("api/dashboard/data/product2sales", views.DashboardProductVsOrderData.as_view(), name="api-dashboard-productvsorder"),
    
    
    
    
    
    path("login", views.admin_login, name="admin-login"),
    
    #admin otp 
    path("login/otp", views.admin_login_otp, name="admin-login-otp"),
    path("login/otp/<uid>", views.admin_login_otp_verify, name="admin-login-otp-verify"),
    
    
    
    
    path("all-users", views.admin_all_users, name="admin-all-users"),
    
    #user management
    path("user/create", views.admin_user_create, name="admin-user-create"),
    path("user/edit/<str:pk>", views.admin_user_edit, name="admin-user-edit"),
    path("user/delete/<str:pk>", views.admin_user_delete, name="admin-user-delete"),
    
    
    #category management
    path("category", categoryView.all_category, name="admin-all-category"),
    path("category/create", categoryView.create_category, name="admin-category-create"),
    path("category/edit/<slug:cat_slug>", categoryView.edit_category, name="admin-category-edit"),
    path("category/delete/<slug:cat_slug>", categoryView.delete_category, name="admin-category-delete"),
    
    #Product management
    
    path("product/create", productView.create_product_with_variant, name="admin-product-create"),
    path("product", productView.all_product, name="admin-all-product"),
    path("product/edit/<slug:product_slug>", productView.edit_product, name="admin-product-edit"),
    path("product/delete/<slug:product_slug>", productView.delete_product, name="admin-product-delete"),
    
    #product varaint management
    path("product/edit/variant/addnew/<slug:product_slug>", productView.add_product_variant, name="admin-product-variant-add"),
    path("product/edit/variant/<slug:product_variant_slug>", productView.edit_product_variant, name="admin-product-variant-edit"),
    path("product/delete/variant/<slug:product_variant_slug>", productView.delete_product_variant, name="admin-product-variant-delete"),
    
    #brand management
    path("brand", extraView.all_brand, name="admin-all-brand"),
    path("brand/create", extraView.create_brand, name="admin-brand-create"),
    # path("category/edit/<slug:cat_slug>", categoryView.edit_category, name="admin-category-edit"),
    # path("category/delete/<slug:cat_slug>", categoryView.delete_category, name="admin-category-delete"),
    
    
    #atribute management
    path("atribute", extraView.all_atribute, name="admin-all-atribute"),
    path("atribute/create", extraView.create_atribute, name="admin-atribute-create"),
  
    #coupon management
    path("coupon", productView.all_coupon, name="admin-all-coupon"),
    path("coupon/create", productView.create_coupon, name="admin-coupon-create"),
    path("coupon/edit/<int:id>", productView.edit_coupon, name="admin-coupon-edit"),
    
    #atribute value management
    path("atribute_value", extraView.all_atribute_value, name="admin-all-atribute_value"),
    path("atribute_value/create", extraView.create_atribute_value, name="admin-atribute_value-create"),
  
    #order management 
    path("all-orders", orderView.all_orders_admin, name="admin-all-orders"),
    path("orders/detail/<str:order_id>", orderView.admin_order_history_detail, name="admin-order-history-detail"),
    path("orders/detail/change/status", orderView.change_order_status_admin, name="change_order_status_admin"),


    #Category offer Management 
    path("all-category-offer", offerView.admin_all_category_offer.as_view(), name="admin-all-category-offer"),
    path("all-category-offer/create", offerView.adminCategoryOfferCreate.as_view(), name="admin-category-offer-create"),
    path("all-category-offer/<int:pk>/update/", offerView.adminCategoryOfferUpdate.as_view(), name="admin-category-offer-update"),
    path("all-category-offer/<int:pk>/delete/", offerView.adminCategoryOfferDelete.as_view(), name="admin-category-offer-delete"),
    

    #Product offer Management 
    path("all-product-offer", offerView.admin_all_product_offer.as_view(), name="admin-all-product-offer"),
    path("all-product-offer/create", offerView.adminProductOfferCreate.as_view(), name="admin-product-offer-create"),
    path("all-product-offer/<int:pk>/update/", offerView.adminProductOfferUpdate.as_view(), name="admin-product-offer-update"),
    path("all-product-offer/<int:pk>/delete/", offerView.adminProductOfferDelete.as_view(), name="admin-product-offer-delete"),
    
    
    #banner Management
    # banner mangement view is under offer management due to classs view
    path("all-banner", offerView.admin_all_banner.as_view(), name="admin-all-banner"),
    path("all-banner/create", offerView.adminBannerCreate.as_view(), name="admin-banner-create"),
    path("all-banner/<int:pk>/update/", offerView.adminBannerUpdate.as_view(), name="admin-banner-update"),
    path("all-banner/<int:pk>/delete/", offerView.adminBannerDelete.as_view(), name="admin-banner-delete"),
    
# 
]