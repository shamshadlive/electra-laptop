from django.shortcuts import render,redirect
from accounts.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import EditUserForm,CreateUserForm
from django.urls import reverse
import functools
# Create your views here.

#decorator for checking admin or not
def check_isadmin(view_func, redirect_url="admin-login"):
    """
        used to check loged one was admin or not
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_authenticated:
            return view_func(request,*args, **kwargs)
        messages.error(request, "You need to be login as admin to access this page")
        redirect_url_ = reverse(redirect_url)+'?next='+request.path
        return redirect(redirect_url_)
    return wrapper






@check_isadmin
def admin_home(request):
    return render(request, 'admincontrol/index.html')

def admin_login(request):
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        if not User.objects.filter(Q(email=email) & Q(is_superuser=1)).exists():
            messages.error(request, "Invalid Username of admin")
            return redirect('admin-login')

        user = authenticate(username=email,password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('admin-login')
        else:
            login(request,user)
            next_url = request.GET.get('next')  # Get the "next" parameter from the form
            print(next_url)
            if next_url:
                print("++++++++++")   
                return redirect(next_url)
            
            return redirect('admin-home')
        
    if request.user.is_authenticated and  request.user.is_superuser:
        return redirect('admin-home')
    
    return render(request, 'admincontrol/login.html')

#==========user management===============
@check_isadmin
def admin_all_users(request):
    users = User.objects.all()
    context = {'users':users}
    return render(request, 'admincontrol/all_users.html',context)


@check_isadmin
def admin_user_create(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data["password"]
            )
            user.is_superuser = form.cleaned_data['is_superuser']
            user.is_email_verified = form.cleaned_data['is_active'] 
            user.is_staff = form.cleaned_data['is_active'] 
            user.is_active = form.cleaned_data['is_active'] 
            
            user.save()
            messages.success(request, "User Created ")
            return redirect('admin-all-users')
        else:
            return render(request, 'admincontrol/user_create.html', {'form': form})
        
    context = {'form':form}
    return render(request, 'admincontrol/user_create.html')


def admin_user_edit(request,pk):
    
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return redirect('admin-all-users')
    except ValueError:
        return redirect('admin-all-users')

    form = EditUserForm(instance=user)
    
    if request.method == 'POST':
        form = EditUserForm(request.POST,instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = form.cleaned_data['is_superuser']
            user.is_active = form.cleaned_data['is_active']
            user.is_email_verified = form.cleaned_data['is_email_verified'] 
            user.is_staff = form.cleaned_data['is_staff'] 
            
            user.save()
            messages.success(request, "User Updated 💡")
            return redirect('admin-user-edit',pk)
        else:
            messages.error(request, form.errors)
            return render(request, 'admincontrol/user_edit.html', {'form': form,'pk':pk})
    context = {'form':form,'pk':pk}
    return render(request, 'admincontrol/user_edit.html',context)

def admin_user_delete(request,pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return redirect('admin-all-users')
    except ValueError:
        return redirect('admin-all-users')
    user.delete()
    messages.error(request, "User Deleted ❌")
    return redirect('admin-all-users')


    