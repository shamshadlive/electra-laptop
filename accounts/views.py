from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate,login
from accounts.models import User
from django.contrib import messages
from .forms  import UserForm
# from verify_email.email_handler import send_verification_email
from accounts.helper.send_verification_email  import CustomVerifyEmail

#forget password 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from cart.models import Cart,CartItem
from cart.views import _cart_id
from django.core.exceptions import ObjectDoesNotExist
import requests
def loginpage (request):
    
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Invalid Email Adress")
            return redirect('login-page')
        
        if not User.objects.filter(email=email,is_email_verified=True,is_active=True).exists():
            messages.error(request, "Email Not Verified Yet !")
            return redirect('login-page')
        
        if not User.objects.filter(email=email,is_active=True).exists():
            messages.error(request, "You are blocked by admin ! Please contact admin")
            return redirect('login-page')
        
        
        user = authenticate(username=email,password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('login-page')
        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)
                    try:
                        user_cart = CartItem.objects.filter(user=user)
                        if user_cart.exists():
                            current_user_cart = user_cart[0].cart  # user's current cart
                            
                            for item in cart_items:
                                matching_user_item = user_cart.filter(product=item.product).first()
                                if matching_user_item:
                                    matching_user_item.quantity += item.quantity
                                    matching_user_item.save()
                                    item.delete()
                                    print("Deleted item")
                                else:
                                    item.user = user
                                    item.cart = current_user_cart
                                    item.save()
                                    print("Moved item to current user's cart")
                        else:
                            raise ObjectDoesNotExist
                    except ObjectDoesNotExist:
                        print("User cart doesn't exist")
                        for item in cart_items:
                            item.user = user
                            item.cart = cart
                            item.save()
            except:
                pass
                
            
            
            
            login(request,user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('home')
            
    
    return render(request, 'accounts/userlogin.html')

def signuppage (request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserForm()
    context = {'form':form}
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if form.is_valid():
            if password != confirm_password:
                messages.error(request, "Password Not Match")
                return render(request, 'accounts/user-signup.html', {'form': form})
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data["password"]
            )
            inactive_user = CustomVerifyEmail.send_verification_email(request, form)
            messages.success(request, "Account Created Succesfuly , Please Activate to Continue")
            return redirect('login-page')
        else:
            return render(request, 'accounts/user-signup.html', {'form': form})
    else:
        form = UserForm()
    
    
    
    return render(request, 'accounts/user-signup.html')


def logout_page(request):
    if request.user.is_superuser:
        logout(request)
        return redirect('admin-login')
    else:
        logout(request)
        return redirect('/')
    

# ==========FORGET PASSWORD =========
def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            
            #SEND FORGOT PASSWORD MAIL
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string ('accounts/reset_password_email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.content_subtype = 'html'
            send_email.send()
            messages.success(request, "Email Has Been Successfully shared , please verify to reset")
            return redirect('login-page')
        else:
            messages.error(request, "Account Not Exists , Please Sign Up")
            
        
    return render(request, 'accounts/forgot-password.html')
    
    
def reset_password_verify(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password")
        return redirect('reset-password')
    else:
        messages.error(request, "Invalid Link ! Expired")
        return redirect('forget-password')
        

def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            try:
                user = User.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, "Resetting Password Completed")
            except User.DoesNotExist:
                messages.error(request, "Error")    
            return redirect('login-page')
        else:
            messages.error(request, "Password Not Match")
            return redirect('reset-password')
            
    return render(request,'accounts/reset-password.html')

