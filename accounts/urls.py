from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.loginpage, name="login-page"),
    path("signup/", views.signuppage, name="signup-page"),
    path("logout/", views.logout_page, name="logout-page"),
    
    # admin login and signup
    
    
]