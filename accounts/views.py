from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate,login
from accounts.models import User
from django.contrib import messages
from .forms  import UserForm

# Create your views here.

def loginpage (request):
    
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Invalid Email Adress")
            return redirect('login-page')
        
        if not User.objects.filter(email=email,is_active=True).exists():
            messages.error(request, "You are blocked by admin ! Please contact admin")
            return redirect('login-page')
        
        if not User.objects.filter(email=email,is_email_verified=True).exists():
            messages.error(request, "Email Not Verified Yet !")
            return redirect('login-page')
        
        
        user = authenticate(username=email,password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('login-page')
        else:
            login(request,user)
            return redirect('home')
    
    return render(request, 'accounts/userlogin.html')

def signuppage (request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserForm()
    context = {'form':form}
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data["password"]
            )
            user.save()
            
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
    

