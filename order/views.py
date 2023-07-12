from django.shortcuts import render,redirect,reverse
from cart.models import CartItem
from .forms import OrderForm,ChangeOrderStatusForm
from .models import Order,Payment,OrderProduct,PaymentMethod
from product_management.models import Product_Variant,Coupon
import datetime
from django.http import JsonResponse
import json
from django.contrib import messages
from accounts.models import AdressBook
import razorpay
from django.conf import settings
from wallet.models import Wallet,WalletTransaction
# Create your views here.


def order_summary(request):
    current_user = request.user
    
    #if cart count <=0 
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count= cart_items.count()
    if cart_count <=0:
        return redirect('cart')
    
    sale_total = 0 
    max_total = 0
    discount = 0
    grand_total =0
    additional_discount = 0
    for cart_item in cart_items:
            sale_total += ( cart_item.product.sale_price * cart_item.quantity)
            max_total += ( cart_item.product.max_price * cart_item.quantity)
            
   
    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        coupon_code = request.POST.get('coupon_code')
        
        if selected_address_id is None:
            messages.error(request, "Please Choose A Address")
            return redirect('checkout')
        
        form = OrderForm(request.POST)
        coupon = False
        if coupon_code:
            try:
                coupon = Coupon.objects.get(coupon_code__iexact=coupon_code,is_active=True)
                if coupon.minimum_amount > sale_total:
                    messages.error(request, "Coupon is Not Applicable For This Order")
                    return redirect('checkout')
                else:
                    additional_discount =  sale_total * coupon.discount_percentage /100
                    sale_total = sale_total - additional_discount
            except Coupon.DoesNotExist:
                messages.error(request, "Coupon is Unavailable")
                return redirect('checkout')
        
        grand_total = sale_total
        discount = max_total - sale_total
        if form.is_valid():
            #store in order table
            data = Order()
            data.user = current_user
            
            #shipping address
            try:
                shipping_address = AdressBook.objects.get(id=selected_address_id)
            except AdressBook.DoesNotExist:
                messages.error(request, "Please Choose A Address")
                return redirect('checkout')
            
            if coupon:
                data.coupon_code = coupon
            
            
            data.additional_discount = additional_discount
            data.shipping_address = shipping_address
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            #generate order number
            current_datetime = datetime.datetime.now()
            current_year = current_datetime.strftime("%Y")
            current_month = current_datetime.strftime("%m")
            current_day = current_datetime.strftime("%d")
            current_hour = current_datetime.strftime("%H")
            current_minute = current_datetime.strftime("%M")
            concatenated_datetime = current_year + current_month + current_day + current_hour + current_minute
            
            order_number = 'ORD'+concatenated_datetime+str(data.id)
            
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            payment_methods = PaymentMethod.objects.filter(is_active=True)
            # window.location.href = `{{success_url}}/?order_id={{order.order_number}}&method=RAZORPAY&payment_id=${response.razorpay_payment_id}&payment_order_id=${response.razorpay_order_id}&payment_sign=${response.razorpay_signature}`
            context = { 
                'order':order,
                'cart_items':cart_items,
                
                'grand_total':grand_total,
                'sale_total':sale_total,
                'max_total':max_total,
                'discount':discount,
                'additional_discount':additional_discount,
                'coupon' : coupon,
                
                
                'shipping_address':shipping_address,
                'payment_methods':payment_methods
            }
            return render(request, 'store/order_summary.html',context)
        else:
            messages.error(request, form.errors)
            return redirect('checkout')
    else:
        return redirect('checkout')
    
    
    



def place_order(request):
    current_user = request.user
    if request.method == 'POST':
        order_number = request.POST.get('order_number_order_summary')
        payment_method = request.POST.get('payment_method')
        wallet_balance_checked = int(request.POST.get('wallet_balance'))
        
        order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
        grand_total = order.order_total
        wallet_discount = 0
        if wallet_balance_checked == 1:
            wallet = Wallet.objects.get(user=current_user,is_active=True)
            if wallet.balance <= grand_total  :  
                grand_total = grand_total- wallet.balance
                order.order_total = grand_total
                order.wallet_discount = wallet.balance
                order.save()   
            else:
                grand_total = 0
                order.wallet_discount = order.order_total
                order.order_total = grand_total
                order.save()
            
        
        try:  
            if grand_total==0:
                raise Exception
            if payment_method == 'RAZORPAY':
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                payment = client.order.create({'amount':float(grand_total) * 100,"currency": "INR"})  
            else:
                payment = False 
        except :
            payment = False 
            
        
            
        
        
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count= cart_items.count()
        if cart_count <=0:
            return redirect('cart')
        
        sale_total = 0 
        max_total = 0
        
        
        for cart_item in cart_items:
                sale_total += ( cart_item.product.sale_price * cart_item.quantity)
                max_total += ( cart_item.product.max_price * cart_item.quantity)
        
        discount = max_total-sale_total
        success_url = request.build_absolute_uri(reverse('payment-success'))
        failed_url = request.build_absolute_uri(reverse('payment-failed'))
        
        context = { 
        'order':order,
        'cart_items':cart_items,
        
        'sale_total':sale_total,
        'max_total':max_total,
        'discount':discount,

        'payment':payment,
        'success_url':success_url,
        'failed_url':failed_url,

        }
        
        return render(request, 'store/payment.html',context)
    



# def place_order(request,quantity=0,cart_items=None):
#     current_user = request.user
    
#     #if cart count <=0 
#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count= cart_items.count()
#     if cart_count <=0:
#         return redirect('cart')
    
#     sale_total = 0 
#     max_total = 0
#     discount = 0
#     grand_total =0
#     additional_discount = 0
#     for cart_item in cart_items:
#             sale_total += ( cart_item.product.sale_price * cart_item.quantity)
#             max_total += ( cart_item.product.max_price * cart_item.quantity)
            
   
#     if request.method == 'POST':
#         selected_address_id = request.POST.get('address')
#         coupon_code = request.POST.get('coupon_code')
        
#         if selected_address_id is None:
#             messages.error(request, "Please Choose A Address")
#             return redirect('checkout')
        
#         form = OrderForm(request.POST)
#         coupon = False
#         if coupon_code:
#             try:
#                 coupon = Coupon.objects.get(coupon_code__iexact=coupon_code,is_active=True)
#                 if coupon.minimum_amount > sale_total:
#                     messages.error(request, "Coupon is Not Applicable For This Order")
#                     return redirect('checkout')
#                 else:
#                     additional_discount =  sale_total * coupon.discount_percentage /100
#                     sale_total = sale_total - additional_discount
#             except Coupon.DoesNotExist:
#                 messages.error(request, "Coupon is Unavailable")
#                 return redirect('checkout')
        
#         grand_total = sale_total
#         discount = max_total - sale_total
#         if form.is_valid():
#             #store in order table
#             data = Order()
#             data.user = current_user
            
#             #shipping address
#             try:
#                 shipping_address = AdressBook.objects.get(id=selected_address_id)
#             except AdressBook.DoesNotExist:
#                 messages.error(request, "Please Choose A Address")
#                 return redirect('checkout')
            
#             if coupon:
#                 data.coupon_code = coupon
            
            
#             data.additional_discount = additional_discount
#             data.shipping_address = shipping_address
#             data.order_note = form.cleaned_data['order_note']
#             data.order_total = grand_total
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()
            
#             #generate order number
#             current_datetime = datetime.datetime.now()
#             current_year = current_datetime.strftime("%Y")
#             current_month = current_datetime.strftime("%m")
#             current_day = current_datetime.strftime("%d")
#             current_hour = current_datetime.strftime("%H")
#             current_minute = current_datetime.strftime("%M")
#             concatenated_datetime = current_year + current_month + current_day + current_hour + current_minute
            
#             order_number = 'ORD'+concatenated_datetime+str(data.id)
            
#             data.order_number = order_number
#             data.save()
            
#             order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
#             client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#             try:
#                 payment = client.order.create({'amount':float(grand_total) * 100,"currency": "INR"})
#             except Exception as e:
#                 payment = False
#             payment_methods = PaymentMethod.objects.filter(is_active=True)
#             # window.location.href = `{{success_url}}/?order_id={{order.order_number}}&method=RAZORPAY&payment_id=${response.razorpay_payment_id}&payment_order_id=${response.razorpay_order_id}&payment_sign=${response.razorpay_signature}`
            
#             success_url = request.build_absolute_uri(reverse('payment-success'))
#             failed_url = request.build_absolute_uri(reverse('payment-failed'))
#             context = { 
#                 'order':order,
#                 'cart_items':cart_items,
                
#                 'grand_total':grand_total,
#                 'sale_total':sale_total,
#                 'max_total':max_total,
#                 'discount':discount,
#                 'additional_discount':additional_discount,
#                 'coupon' : coupon,
                
                
#                 'shipping_address':shipping_address,
#                 'payment':payment,
#                 'success_url':success_url,
#                 'failed_url':failed_url,
#                 'payment_methods':payment_methods
#             }
#             return render(request, 'store/payment.html',context)
#         else:
#             messages.error(request, form.errors)
#             return redirect('checkout')
#     else:
#         return redirect('checkout')

            

            
      
def payment_success(request):
    method = request.GET.get('method')
    payment_id = request.GET.get('payment_id')
    payment_order_id = request.GET.get('payment_order_id')
    order_id = request.GET.get('order_id')
    payment_sign = request.GET.get('payment_sign')

    if method == 'COD':
        try:
            order = Order.objects.get(user=request.user,is_ordered=False,order_number=order_id)
        except Exception:
            return redirect('home')
        payment_method_is_active = PaymentMethod.objects.filter(method_name=method,is_active=True).exists()
        if payment_method_is_active:
            payment = Payment(
                user=request.user,
                payment_id='PID-COD'+order_id,
                payment_order_id = order_id,
                payment_signature='Signed',   
                payment_method=method,
                amount_paid=order.order_total,
                payment_status='SUCCESS',
            )
            payment.save()
        
            wallet = Wallet.objects.get(user=request.user,is_active=True)
            wallet.balance = wallet.balance - order.wallet_discount
            wallet.save()
            
            wallet_transaction = WalletTransaction.objects.create(wallet=wallet,
                                                               transaction_type='DEBIT',
                                                               transaction_detail=str(order.order_number),
                                                               amount=order.wallet_discount)
            wallet_transaction.save()
            
            order.payment = payment
            order.is_ordered = True
            order.save()
            
            #move cart items to order product table
            cart_items = CartItem.objects.filter(user=request.user)
            
            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                orderproduct.user_id = request.user.id
                orderproduct.product_id = item.product.id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.sale_price
                orderproduct.ordered = True
                orderproduct.save()
                
                #reduce the quantity of soled produce
                
                product = Product_Variant.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()
            
            #clear the cart
            CartItem.objects.filter(user=request.user).delete()
            
            request.session["order_number"] = order_id
            request.session["payment_id"] = 'PID-COD'+order_id
            return redirect('order_complete')
        else:
            messages.error(request, "Invalid Payment Method Found")
            return redirect('payment-failed')

    elif method == 'RAZORPAY':
        order = Order.objects.get(user=request.user,is_ordered=False,order_number=order_id)
        payment_method_is_active = PaymentMethod.objects.filter(method_name=method,is_active=True).exists()
        if payment_method_is_active:
            payment = Payment(
                user=request.user,
                payment_id=payment_id,
                payment_order_id = payment_order_id,
                payment_signature=payment_sign,   
                payment_method=method,
                amount_paid=order.order_total,
                payment_status='SUCCESS',
            )
            payment.save()
            
            wallet = Wallet.objects.get(user=request.user,is_active=True)
            wallet.balance = wallet.balance - order.wallet_discount
            wallet.save()
            
            wallet_transaction = WalletTransaction.objects.create(wallet=wallet,
                                                               transaction_type='DEBIT',
                                                               transaction_detail=str(order.order_number),
                                                               amount=order.wallet_discount)
            wallet_transaction.save()
            
            
            order.payment = payment
            order.is_ordered = True
            order.save()
            
            #move cart items to order product table
            cart_items = CartItem.objects.filter(user=request.user)
            
            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                orderproduct.user_id = request.user.id
                orderproduct.product_id = item.product.id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.sale_price
                orderproduct.ordered = True
                orderproduct.save()
                
                #reduce the quantity of soled produce
                
                product = Product_Variant.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()
            
            #clear the cart
            CartItem.objects.filter(user=request.user).delete()
            
            request.session["order_number"] = order_id
            request.session["payment_id"] = payment_id
            return redirect('order_complete')
        else:
            messages.error(request, "Invalid Payment Method Found")
            return redirect('payment-failed')
    else:
        return redirect('user-dashboard')
    
def payment_failed(request):
    context = {
    'method': request.GET.get('method'),
    'error_code': request.GET.get('error_code'),
    'error_description': request.GET.get('error_description'),
    'error_reason': request.GET.get('error_reason'),
    'error_payment_id': request.GET.get('error_payment_id'),
    'error_order_id': request.GET.get('error_order_id')
    }
    return render(request, 'store/payment_failed.html',context)
    
    
    
    
    
    
    
def order_complete(request):
    try: 
        if(request.session['order_number'] and request.session["payment_id"]):
            order_number= request.session['order_number']  
            payment_id=request.session['payment_id']
            
            try:
                order = Order.objects.get(order_number=order_number,is_ordered=True)
                ordered_products = OrderProduct.objects.filter(order_id=order.id)
                sub_total = 0
                max_total = 0
                for i in ordered_products:
                    sub_total += i.product_price * i.quantity
                    max_total += i.product.max_price * i.quantity
                payment = Payment.objects.get(payment_id=payment_id)
                context = {
                    'order':order,
                    'order_number':order_number,
                    'payment':payment,
                    'sub_total':sub_total,
                    'max_total':max_total,
                    'discount':(max_total-sub_total),
                    'ordered_products':ordered_products
                }
                del request.session['order_number']
                del request.session['payment_id']
                return render(request, 'store/order_complete.html',context)
            except Exception as e:
                print(e)
                return redirect('home')
            
                
    except Exception as e:
        print(e)
        return redirect('home')
    
def order_cancel_user(request,order_id):
    order = Order.objects.get(user=request.user,order_number=order_id)
    if not order.order_status=='Cancelled_User':
        order.order_status='Cancelled_User'
        order.save()
        wallet = Wallet.objects.get(user=request.user,is_active=True)
        wallet.balance += (order.order_total + order.wallet_discount)
        wallet.save()
        
        wallet_transaction = WalletTransaction.objects.create(wallet=wallet,
                                                                transaction_type='CREDIT',
                                                                transaction_detail=str(order.order_number)+'  CANCELLED',
                                                                amount=order.wallet_discount)
        wallet_transaction.save()
        return redirect('order-history-detail',order_id=order.order_number)
    else:
        return redirect('order-history-detail',order_id=order.order_number)
    
    
def order_return_user(request,order_id):
    
    order = Order.objects.get(user=request.user,order_number=order_id)
    if not order.order_status=='Returned_User':
        order.order_status='Returned_User'
        order.save()
        wallet = Wallet.objects.get(user=request.user,is_active=True)
        wallet.balance += (order.order_total + order.wallet_discount)
        wallet.save()
        
        wallet_transaction = WalletTransaction.objects.create(wallet=wallet,
                                                                transaction_type='CREDIT',
                                                                transaction_detail=str(order.order_number)+'  RETURNED',
                                                                amount=order.wallet_discount)
        wallet_transaction.save()
        return redirect('order-history-detail',order_id=order.order_number)
    else:
        return redirect('order-history-detail',order_id=order.order_number)
    
    
    
    
    
#ADMIN  SIDE ORDER MANAGEMENT

def all_orders_admin(request):
    order_status = request.GET.get('status')
    print(order_status)
    if order_status:
        orders = Order.objects.filter(order_status__icontains=order_status).order_by('-created_at')
    else: 
        orders = Order.objects.all().order_by('-created_at')
        
    context={
        'orders':orders
    }
    return render(request, 'admincontrol/all_orders.html',context)


def admin_order_history_detail(request,order_id):
    order = Order.objects.get(order_number=order_id)
    order_products = OrderProduct.objects.filter(order=order)
    payment = Payment.objects.filter(payment_id=order.payment)[0]
    form = ChangeOrderStatusForm(instance=order)
    context ={
        'order':order,
        'order_products':order_products,
        'payment':payment,
        'form':form,
    }
    return render(request, 'admincontrol/order_details.html',context)
    

def change_order_status_admin(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == "POST" and is_ajax:
        data = json.load(request)
        order_number = data.get('order_number')
        selected_option = data.get('selected_option')
        # Update the order status based on the order_number and selected_option
        try:
            order = Order.objects.get(order_number=order_number)
            order.order_status = selected_option
            order.save()
            return JsonResponse({"status": "success","selected_option":selected_option})
        except Order.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Order Not Found"})
        # Return a JSON response indicating success or failure
        
    else:
        # Return a JSON response indicating an invalid request
        return JsonResponse({"status": "error", "message": "Invalid request"})
    