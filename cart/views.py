from django.shortcuts import render,redirect,get_object_or_404,reverse
from product_management.models import Product_Variant,Coupon
from .models import Cart,CartItem,Wishlist,WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import AdressBook
from accounts.forms import AdressBookForm
import json
from django.http import JsonResponse

# Create your views here.

#to get the cart id if present
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart(request,total=0,quantity=0,cart_items=None):
    total_with_orginal_price =0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        
        for cart_item in cart_items:
            total += ( cart_item.product.sale_price * cart_item.quantity)
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity
            
    except ObjectDoesNotExist:
        pass
    
    discount = total_with_orginal_price - total
    grand_total = total
    
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'grand_total':grand_total,
        'discount':discount,
        'total_with_orginal_price':total_with_orginal_price
    }
    return render(request, 'store/cart.html',context)



def add_cart(request,product_id):
    
    current_user = request.user
    product = Product_Variant.objects.get(id=product_id)    #get the product
    #if user authenticated
    if current_user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # to get the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        
        
        try:
            cart_item = CartItem.objects.get(product=product , user=current_user)
            cart_item.quantity +=1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                user=current_user,
                cart=cart,
                quantity = 1,
            )
            cart_item.save()
        return redirect('cart')
        
    else:
        
    # ===CART CREATED ===
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # to get the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        
        # ===Product saved to cart item
        try:
            cart_item = CartItem.objects.get(product=product , cart=cart)
            cart_item.quantity +=1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity = 1,
            )
            cart_item.save()
        return redirect('cart')



def remove_cart(request,product_id):
    product = get_object_or_404(Product_Variant,id=product_id)   #get the product
    
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user) # to get the cartid present in the session
    else:  
        cart = Cart.objects.get(cart_id=_cart_id(request)) # to get the cartid present in the session
        cart_item = CartItem.objects.get(product=product,cart=cart)
   
    
    if cart_item.quantity>1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')

def remove_cart_item(request,product_id):
    product = get_object_or_404(Product_Variant,id=product_id)   #get the product

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user) # to get the cartid present in the session
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # to get the cartid present in the session
        cart_item = CartItem.objects.get(product=product,cart=cart)
    
    cart_item.delete()
    
    return redirect('cart')  

@login_required(login_url='login-page')
def checkout(request,total=0,quantity=0,cart_items=None):
    total_with_orginal_price=0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += ( cart_item.product.sale_price * cart_item.quantity)
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity
            product = Product_Variant.objects.get(id=cart_item.product.id)
            if (product.stock - cart_item.quantity) < 0:
                error_message = f'{product.get_product_name()} [{cart_item.quantity}] Stock , Not Available , Please Remove and continue'
                messages.error(request, error_message)
                return redirect('cart')
            
        
    except ObjectDoesNotExist:
        pass
    adress_form = AdressBookForm()
    discount = total_with_orginal_price - total
    grand_total = total
    addreses = AdressBook.objects.filter(user=request.user,is_active=True).order_by('-is_default')
    coupons = Coupon.objects.filter(is_active=True)
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'total_with_orginal_price':total_with_orginal_price,
        'grand_total':grand_total,
        'discount':discount,
        'addreses':addreses,
        'adress_form':adress_form,
        'coupons':coupons
    }
    return render(request, 'store/checkout.html',context)


def coupon_verify(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == "POST" and is_ajax:
        data = json.load(request)
        coupon_code = data.get('coupon_code')
        
        # Update the order status based on the order_number and selected_option
        coupon = Coupon.objects.filter(coupon_code__iexact=coupon_code,is_active=True)
        if not coupon.exists():
            return JsonResponse({"status": "error", "message": "Invalid Coupon"})
        grand_total=0
        cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        for cart_item in cart_items:
            grand_total += ( cart_item.product.sale_price * cart_item.quantity)
        if coupon[0].minimum_amount > grand_total:
             return JsonResponse({"status": "error", "message": "Minimum Purchase amount "+str(coupon[0].minimum_amount)})
        
        
        return JsonResponse({"status": "success",
                             "message":"Coupon Applied "+str(coupon[0].discount_percentage)+"% Offer",
                             "coupon_code":coupon[0].coupon_code,
                             "grand_total":grand_total,
                             "discount_percentage":coupon[0].discount_percentage})
       
        
    else:
        # Return a JSON response indicating an invalid request
        return JsonResponse({"status": "error", "message": "Invalid request"})
    

def add_whishlist(request):
    
    if not request.user.is_authenticated:
        login_url = reverse('login-page')
        
        return JsonResponse({"status": "error", "message": "user not authenticated","user":0,"login_url":login_url})
    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == "POST" and is_ajax:
        data = json.load(request)
        variant = data.get('variant')
        wishlist,created = Wishlist.objects.get_or_create(user=request.user)
        try:
            product_variant = Product_Variant.objects.get(id=variant)
        except :
            return JsonResponse({"status": "error", "message": "Product Not Found"})
        
        wishlist_Item,created = WishlistItem.objects.get_or_create(wishlist=wishlist,product=product_variant)
        if not created:
            wishlist_Item.delete()
        # Update the order status based on the order_number and selected_option
       
        return JsonResponse({"status": "success"})
        
    else:
        # Return a JSON response indicating an invalid request
        return JsonResponse({"status": "error", "message": "Invalid request"})
    