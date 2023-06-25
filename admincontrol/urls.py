from django.urls import path

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
    
    
    
    

]