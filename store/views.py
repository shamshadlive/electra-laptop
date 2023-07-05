from django.shortcuts import render,get_object_or_404,redirect
from product_management.models import Product_Variant
from categoryManagement.models import Category
from cart.models import CartItem,Cart
from cart.views import _cart_id
from django.contrib.auth.decorators import login_required
from order.models import Order,OrderProduct,Payment
# Create your views here.


def home (request):
    return render(request, 'store/home.html')

def store (request,category_slug=None):
    categories = None
    product_variants = None
    
    if category_slug !=None:
        category = get_object_or_404(Category,cat_slug=category_slug)
        product_variants = Product_Variant.objects.select_related('product').prefetch_related('atributes').filter(product__product_catg=category,is_active=True)
        product_variants_count = product_variants.count()
    else:
        product_variants = Product_Variant.objects.select_related('product').prefetch_related('atributes').filter(is_active=True)
        product_variants_count = product_variants.count()
    context = {'product_variants':product_variants,
               'product_variants_count':product_variants_count}
    return render(request, 'store/store.html',context)

def product_variant_detail(request,category_slug,product_variant_slug):
    single_product_variant=None
    try:
        single_product_variant = Product_Variant.objects.select_related('product').prefetch_related('atributes','additional_product_images').get(
                            product__product_catg__cat_slug=category_slug,
                            product_variant_slug=product_variant_slug,
                            is_active=True)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product_variant).exists()
    except Exception as e:
        print(e)
        return redirect('store')
    
    product_variants = Product_Variant.objects.filter(product=single_product_variant.product)
    product_variants_count=product_variants.count()
   
    
    context = { 'single_product_variant' :single_product_variant,
               'product_variants':product_variants,
               'product_variants_count':product_variants_count,
               'in_cart':in_cart}
    
    return render(request, 'store/product_variant_detail.html',context)

#USER DASHBOARD
@login_required(login_url='login-page')
def user_dashboard(request):
    
    return render(request, 'store/dashboard.html')
    
@login_required(login_url='login-page')
def order_history(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context = {
        'orders':orders,
    }
    return render(request, 'store/order_history.html',context)
    
    
@login_required(login_url='login-page')
def order_history_detail(request,order_id):
    order = Order.objects.get(user=request.user,order_number=order_id)
    order_products = OrderProduct.objects.filter(user=request.user,order=order)
    payment = Payment.objects.get(user=request.user,payment_id=order.payment)
    
    context ={
        'order':order,
        'order_products':order_products,
        'payment':payment
    }
    return render(request, 'store/order_detail.html',context)
    
    
    