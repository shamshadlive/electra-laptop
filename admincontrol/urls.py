from django.urls import path
from categoryManagement import views as categoryView
from product_management import views as productView
from extra_management import views as extraView
from . import views
urlpatterns = [
    path("", views.admin_home, name="admin-home"),
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
    
    
    
    
    
    

]