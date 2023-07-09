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
    
    
    #user field update ajax
    path("users/basic/update", views.update_fields_user, name="update_fields_user"),
    path("users/basic/changepassword", views.change_user_password_with_oldpass, name="change_user_password_with_oldpass"),

    path("users/resetpassword/verify/otp/", views.change_user_password_with_email, name="change_user_password_with_email"),
    path("users/resetpassword/otp/<uid>", views.change_user_password_with_email_verify, name="change_user_password_with_email_verify"),
    
    path("users/update/email", views.change_email_with_email, name="change_email_with_email"),
    path("users/update/email/verify", views.change_email_with_email_verify, name="change_email_with_email_verify"),
    
    path("users/update/mobile", views.change_mobile_with_otp, name="change_mobile_with_otp"),
    path("users/update/mobile/verify", views.change_mobile_with_otp_verify, name="change_mobile_with_otp_verify"),
    
    
]