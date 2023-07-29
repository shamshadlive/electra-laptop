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
from django.db.models import Q,Case, When, F, FloatField, Sum,ExpressionWrapper ,DecimalField,Avg,Count
from .models import Banner,ReviewRating,RecentViewedProduct
from order.models import OrderProduct
from .forms import ReviewForm
from datetime import datetime
import json
from django.http import JsonResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.contrib import messages
# Create your views here.



def home (request):
    banners = Banner.objects.filter(is_active=True)
    product_variants = Product_Variant.objects.select_related('product').prefetch_related('atributes').filter(is_active=True).annotate(avg_rating=Avg('product_review__rating')).order_by('-avg_rating')[:10]
    if request.user.is_authenticated:
        recent_viewed_products = RecentViewedProduct.objects.select_related('product').prefetch_related('product__atributes').filter(user=request.user).order_by('-updated_at')[:6]
    else:
        recent_viewed_products=None
    print(recent_viewed_products)
    most_moving_product_variants = Product_Variant.objects.all().annotate(total_orders=Count('orderproduct__order', distinct=True)).order_by('-total_orders')[:6]

   
    context={
        'banners':banners,
        'product_variants':product_variants,
        'recent_viewed_products':recent_viewed_products,
        'most_moving_product_variants':most_moving_product_variants
    }
    return render(request, 'store/home.html',context)


def autocomplete(request):
    if 'term' in request.GET:
        search_query = request.GET.get('term')
        product_variants = Product_Variant.objects.filter(is_active=True)
        
         #search
        terms = search_query.split()  # Split the search query into individual terms
        for term in terms:
            product_variants = [
                            product for product in product_variants
                            if term.lower() in product.get_product_name().lower()
                        ]
            
        
        title = []
        title += [ x.get_product_name() for x in product_variants ]
        return JsonResponse(title,safe=False)
    else:
        return JsonResponse({
            'status':400
        })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def store (request,category_slug=None):
    categories = None
    product_variants = None
    search_query = request.GET.get('query')
    price_min = request.GET.get('price-min')
    price_max = request.GET.get('price-max')
    ratings = request.GET.getlist('RATING')
    
    
    if category_slug !=None:
        try:
            category = get_object_or_404(Category,cat_slug=category_slug)
        except Exception as e:
                print(e)
                return redirect('store')
        product_variants = Product_Variant.objects.select_related('product').prefetch_related('atributes').filter(product__product_catg=category,is_active=True)
        product_variants_count = product_variants.count()
    else:
        product_variants = Product_Variant.objects.select_related('product').prefetch_related('atributes').filter(is_active=True).annotate(avg_rating=Avg('product_review__rating'))

        product_variants_count = product_variants.count()

 
    #search
    if search_query:
        terms = search_query.split()  # Split the search query into individual terms
        for term in terms:
            product_variants = [
                            product for product in product_variants
                            if term.lower() in product.get_product_name().lower()
                        ]
       
    #ratings filter   
    if ratings:
        rating_filters = Q()
        for rating in ratings:
            rating_filters |= Q(avg_rating__gte=rating)

        product_variants = product_variants.filter(rating_filters)
    
    
    
    #price filter 
    if price_min:
        product_variants = product_variants.filter(sale_price__gte=price_min)
    if price_max:
        product_variants = product_variants.filter(sale_price__lte=price_max)
        
        
    # Get all attribute names from the request avoid certain parameters
    attribute_names = [key for key in request.GET.keys() if key not in ['query','page','price-min','price-max','RATING']]
    
    #other filter
    for attribute_name in attribute_names:
        attribute_values = request.GET.getlist(attribute_name)
        if attribute_values:
            product_variants=product_variants.filter(atributes__atribute_value__in=attribute_values)
    
    
    
    
    
    product_variants_count = len(product_variants)
    
  
    # paginator start
    paginator = Paginator(product_variants,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    context = {'product_variants':paged_products,
               'product_variants_count':product_variants_count,
               'search_query':search_query,
               'price_min':price_min,
               'price_max':price_max,
               }
    
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
    
    if request.user.is_authenticated:
        try:
            #recent viewed product add
            recent_viewed,created = RecentViewedProduct.objects.get_or_create(user=request.user,product=single_product_variant)
            if not created:
                recent_viewed.updated_at = datetime.now()
                recent_viewed.save()
            print(recent_viewed)  
            order_product = OrderProduct.objects.filter(user=request.user,product_id=single_product_variant.id).exists()
              
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None
    
    
    product_variants = Product_Variant.objects.filter(product=single_product_variant.product,is_active=True)
    product_variants_count=product_variants.count()
   
    reviews = ReviewRating.objects.filter(is_active=True,product_id=single_product_variant.id).order_by('-updated_at')
    
    context = { 'single_product_variant' :single_product_variant,
               'product_variants':product_variants,
               'product_variants_count':product_variants_count,
               'in_cart':in_cart,
               'order_product':order_product,
               'reviews':reviews,
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
    
    wishlist,created = Wishlist.objects.get_or_create(user=request.user)
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


#=======SUBMIT REVIEW ========
def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form = ReviewForm(request.POST,instance=reviews)
            if form.is_valid():
                form.save()
                messages.success(request, "Thank You ! Review Updated")
                return redirect(url)
            else:
                messages.error(request, form.errors)
                return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = ReviewRating()
                review.subject = form.cleaned_data['subject']
                review.rating = form.cleaned_data['rating']
                review.review = form.cleaned_data['review']
                review.product_id = product_id
                review.user_id = request.user.id
                review.save()
                messages.success(request, "Thank You ! Review Posted")
                return redirect(url)
            else:
                messages.error(request, form.errors.values)
                return redirect(url)
        
    