from django.shortcuts import render,get_object_or_404,redirect
from product_management.models import Product_Variant
from categoryManagement.models import Category
from cart.models import CartItem,Cart,Wishlist,WishlistItem
from cart.views import _cart_id
from django.contrib.auth.decorators import login_required
from order.models import Order,OrderProduct,Payment
from accounts.models import AdressBook
from accounts.forms import AdressBookForm
from django.views.decorators.cache import cache_control
from django.db.models import Q

from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.



def home (request):
    
    return render(request, 'store/home.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def store (request,category_slug=None):
    categories = None
    product_variants = None
    search_query = request.GET.get('query')
    price_min = request.GET.get('price-min')
    price_max = request.GET.get('price-max')
    
    if category_slug !=None:
        category = get_object_or_404(Category,cat_slug=category_slug)
        product_variants = Product_Variant.objects.select_related('product').prefetch_related('atributes').filter(product__product_catg=category,is_active=True)
        product_variants_count = product_variants.count()
    else:
        product_variants = Product_Variant.objects.select_related('product').prefetch_related('atributes').filter(is_active=True)
        product_variants_count = product_variants.count()
    
    #wishlist
    if request.user.is_authenticated:  
        wishlist,created= Wishlist.objects.get_or_create(user=request.user)
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True).values_list('product_id', flat=True)
    else:
        wishlist_items =[]
    
    print(wishlist_items)
        
        
    #search
    if search_query:
        product_variants = product_variants.filter(
            Q(product__product_name__icontains=search_query) |
            Q(product__product_catg__cat_name__icontains=search_query) |
            Q(product__product_brand__brand_name__icontains=search_query) |
            Q(product__product_description__icontains=search_query)
        )
       
    #price filter 
    if price_min:
        product_variants = product_variants.filter(sale_price__gte=price_min)
    if price_max:
        product_variants = product_variants.filter(sale_price__lte=price_max)
        
        
    # Get all attribute names from the request avoid certain parameters
    attribute_names = [key for key in request.GET.keys() if key not in ['query','page','price-min','price-max']]
    
    #other filter
    for attribute_name in attribute_names:
        attribute_values = request.GET.getlist(attribute_name)
        if attribute_values:
            product_variants=product_variants.filter(atributes__atribute_value__in=attribute_values)
    
    product_variants_count = product_variants.count()
    
    # paginator start
    paginator = Paginator(product_variants,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    context = {'product_variants':paged_products,
               'product_variants_count':product_variants_count,
               'search_query':search_query,
               'price_min':price_min,
               'price_max':price_max,
               'wishlist_items':wishlist_items}
    
    return render(request, 'store/store.html',context)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_variant_detail(request,category_slug,product_variant_slug):
    single_product_variant=None
    try:
        single_product_variant = Product_Variant.objects.select_related('product').prefetch_related('atributes','additional_product_images').get(
                            product__product_catg__cat_slug=category_slug,
                            product_variant_slug=product_variant_slug,
                            is_active=True)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product_variant).exists()
        try:
            wishlist,created = Wishlist.objects.get_or_create(user=request.user)
            in_whislist = WishlistItem.objects.filter(wishlist=wishlist,product=single_product_variant).exists()
        except:
            in_whislist = False
    except Exception as e:
        print(e)
        return redirect('store')
    
    product_variants = Product_Variant.objects.filter(product=single_product_variant.product,is_active=True)
    product_variants_count=product_variants.count()
   
    
    context = { 'single_product_variant' :single_product_variant,
               'product_variants':product_variants,
               'product_variants_count':product_variants_count,
               'in_cart':in_cart,
               'in_whislist':in_whislist}
    
    return render(request, 'store/product_variant_detail.html',context)

#USER DASHBOARD
@login_required(login_url='login-page')
def user_dashboard(request):
    
    return render(request, 'store/dashboard.html')
    
@login_required(login_url='login-page')
def order_history(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    orders_count = orders.count()
    paginator = Paginator(orders,10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    context = {
        'orders':paged_products,
        'orders_count':orders_count
        
    }
    return render(request, 'store/order_history.html',context)
    
@login_required(login_url='login-page')
def user_wishlist(request):
    wishlist = Wishlist.objects.get(user=request.user)
    wishlistItems = WishlistItem.objects.filter(wishlist=wishlist,is_active=True).order_by('-created_at')
    wishlistItems_count = wishlistItems.count()
    
    paginator = Paginator(wishlistItems,10)
    page = request.GET.get('page')
    paged_wishlist = paginator.get_page(page)
    
    context = {
        'wishlistItems':paged_wishlist,
        'wishlistItems_count':wishlistItems_count
    }
    return render(request, 'store/wishlist.html',context)
    
@login_required(login_url='login-page')
def order_history_detail(request,order_id):
    try:
        order = Order.objects.get(user=request.user,order_number=order_id)
        order_products = OrderProduct.objects.filter(user=request.user,order=order)
     
        payment = Payment.objects.get(user=request.user,payment_id=order.payment)
    except Order.DoesNotExist:
        return redirect('store')  
    context ={
        'order':order,
        'order_products':order_products,
        'payment':payment,
    }
    return render(request, 'store/order_detail.html',context)
    
    
    
    
@login_required(login_url='login-page')
def user_address(request):
    adress_form = AdressBookForm()
    addreses = AdressBook.objects.filter(user=request.user,is_active=True).order_by('-is_default')
    context ={
        'addreses':addreses,
        'adress_form':adress_form
    }
    return render(request, 'store/address.html',context)
    
    
    
    
    
@login_required(login_url='login-page')
def user_address_create(request,checkout):  
    if request.method == 'POST':
        adress_form = AdressBookForm(request.POST)
        if adress_form.is_valid():
            address = adress_form.save(commit=False)
            address.user = request.user
            address.save()
            print("===========================")
            print(checkout)
            if checkout == 'checkout':
                print("okeeee")
                return redirect('checkout')
            else:
                return redirect('user-address')
        else:
            context ={
                    'adress_form':adress_form
                }
            return render(request, 'store/address.html',context)

@login_required(login_url='login-page')
def user_address_make_default(request,adress_id):
    try:  
        addreses = AdressBook.objects.get(user=request.user,id=adress_id)
        addreses.is_default = True
        addreses.save()
        return redirect('user-address')
    except AdressBook.DoesNotExist:
        return redirect('user-address')

@login_required(login_url='login-page')
def user_address_delete(request,adress_id):
    try:  
        addreses = AdressBook.objects.get(user=request.user,id=adress_id)
        addreses.is_active=False
        addreses.save()
        return redirect('user-address')
    except AdressBook.DoesNotExist:
        return redirect('user-address')

    