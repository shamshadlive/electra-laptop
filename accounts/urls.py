from django.urls import path

from . import views
from accounts.helper.receive_verification_mail import receive_verification_mail
urlpatterns = [
    path("login/", views.loginpage, name="login-page"),
    path("signup/", views.signuppage, name="signup-page"),
    path("logout/", views.logout_page, name="logout-page"),
    
    #verify user and activate
    
    path(f'verification/user/verify-email/<useremail>/<usertoken>/custom', receive_verification_mail, name='verify-email'),
    
    #forget password
    
    path("forgetpassword/", views.forget_password, name="forget-password"),
    path("reset/password/<uidb64>/<token>/", views.reset_password_verify, name="reset-password-verify"),
    path("resetpassword", views.resetpassword, name="reset-password"),
    
    
]