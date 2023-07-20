from django.shortcuts import render,redirect
from accounts.models import User,UserOtp
from django.db.models import Q,Sum,Count
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import EditUserForm,CreateUserForm
from django.urls import reverse
import functools,random
from accounts.helper.message_handler import MessageHandler
from order.models import Order,Payment
from product_management.models import Product_Variant,Brand,Coupon
from categoryManagement.models import Category
from rest_framework.views import APIView
from rest_framework.response import Response
from store.models import Banner
from offer_management.models import CategoryOffer
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
    users_count = User.objects.filter(is_active=True).count()
    sales = Order.objects.filter(is_ordered=True).exclude(order_status__in=["Cancelled_Admin", "Cancelled_User", "Returned_User"]).aggregate(total_sales=Sum('order_total'))
    total_sales = 0
    if sales['total_sales'] is not None:
        total_sales = float(sales['total_sales'])

    active_products_count = Product_Variant.objects.filter(is_active=True,product__is_active=True).count()
    
    new_orders_count = Order.objects.filter(is_ordered=True,order_status='New').count()
    
    brand_count = Brand.objects.filter(is_active=True).count()
    coupon_count = Coupon.objects.filter(is_active=True).count()
    categories_count = Category.objects.filter(is_active=True).count()
    banner_count = Banner.objects.filter(is_active=True).count()
    offer_count = CategoryOffer.objects.filter(is_active=True).count()
    
    
    recent_signups = User.objects.all().order_by('-date_joined')[:10]
    recent_payments = Payment.objects.all().order_by('-payment_order_id')[:10]
    
    context = {
        'users_count':users_count,
        'total_sales':total_sales,
        'active_products_count':active_products_count,
        'new_orders_count':new_orders_count,
        'brand_count':brand_count,
        'coupon_count':coupon_count,
        'categories_count':categories_count,
        'categories_count':categories_count,
        'banner_count':banner_count,
        'offer_count':offer_count,
        'recent_signups':recent_signups,
        'recent_payments':recent_payments
    }
    return render(request, 'admincontrol/index.html',context)



#dashboard api

class DashboardSalesData(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request, format=None):
        total_orders_count  = Order.objects.filter(is_ordered=True).count()
        new_orders_count  = Order.objects.filter(is_ordered=True,order_status='New').count()
        cancelled_orders_count  = Order.objects.filter(is_ordered=True,order_status__in=["Cancelled_Admin", "Cancelled_User"]).count()
        returned_orders_count  = Order.objects.filter(is_ordered=True,order_status='Returned_User').count()
        delivered_orders_count  = Order.objects.filter(is_ordered=True,order_status='Delivered').count()
        data = {
            'status':'success',
            'data':{
                'Total Orders':total_orders_count,
                'New Orders':new_orders_count,
                'cancelled Orders':cancelled_orders_count,
                'Returned Orders':returned_orders_count,
                'Delivered Orders':delivered_orders_count,
                }    
        }
        return Response(data)

class DashboardProductVsOrderData(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request, format=None):
        products_with_order_count = Product_Variant.objects.all().annotate(total_orders=Count('orderproduct__order', distinct=True)).order_by('-total_orders')[:10]
        # Create a dictionary with product names and their total order counts
        product_order_counts = {product.get_product_name()[:20]+'...': product.total_orders for product in products_with_order_count}
        print(product_order_counts)
        data = {
            'status':'success',
            'data':product_order_counts  
        }
        return Response(data)















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


def admin_login_otp(request):
    if request.method=="POST":
        if not User.objects.filter(phone_number__iexact=request.POST['phone_number'],is_superuser=True).exists():
            messages.error(request, "Invalid Admin Phone Number")
            return render(request, 'admincontrol/login_otp.html')
        user = User.objects.get(phone_number=request.POST['phone_number'])
        otp=random.randint(1000,9999)
        user_otp,created = UserOtp.objects.update_or_create(user=user, defaults={'otp': f'{otp}'})
        try:
            messagehandler=MessageHandler(request.POST['phone_number'],otp).send_otp_via_message()
        except Exception as e:
            messages.error(request, "Unable To Send OTP Contact Admin")
            return render(request, 'admincontrol/login_otp.html')
            
        red=redirect(f'otp/{user_otp.uid}')
        red.set_cookie("can_otp_enter",True,max_age=600)
        return red
    
    return render(request, 'admincontrol/login_otp.html')
    
def admin_login_otp_verify(request,uid):
    if request.method=="POST":
        userOtp=UserOtp.objects.get(uid=uid)     
        if request.COOKIES.get('can_otp_enter')!=None:
            if(userOtp.otp==request.POST['otp']):
                login(request,userOtp.user)
                red=redirect("admin-home")
                red.set_cookie('verified',True)
                return red
            else:
                messages.error(request, "Invalid OTP")
                return render(request,"admincontrol/login_otp_verify.html",{'id':uid})
        else:
            messages.error(request, "10 mins Over ! Time Exceeded")
            return render(request,"admincontrol/login_otp_verify.html",{'id':uid})
                
    return render(request,"admincontrol/login_otp_verify.html",{'id':uid})
    


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


    