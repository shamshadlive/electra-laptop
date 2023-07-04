from django.shortcuts import render,redirect,get_object_or_404
from product_management.models import Product_Variant
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.

#to get the cart id if present
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart(request,total=0,quantity=0,cart_items=None):
    
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        
        for cart_item in cart_items:
            total += ( cart_item.product.sale_price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    
    discount = 0
    grand_total = total+discount
    
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'grand_total':grand_total,
        'discount':discount
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
    
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        
        for cart_item in cart_items:
            total += ( cart_item.product.sale_price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    
    discount = 0
    grand_total = total+discount
    
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'grand_total':grand_total,
        'discount':discount
    }
    return render(request, 'store/checkout.html',context)
