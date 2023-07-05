from django.shortcuts import render,redirect
from cart.models import CartItem
from .forms import OrderForm,ChangeOrderStatusForm
from .models import Order,Payment,OrderProduct
from product_management.models import Product_Variant
import datetime
from django.http import JsonResponse
import json



# Create your views here.

def place_order(request,total=0,quantity=0,cart_items=None):
    current_user = request.user
    
    #if cart count <=0 
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count= cart_items.count()
    if cart_count <=0:
        return redirect('cart')
    
    for cart_item in cart_items:
            total += ( cart_item.product.sale_price * cart_item.quantity)
    
    grand_total=0
    discount=0
    grand_total = discount+total
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #store in order table
            data = Order()
            data.user = current_user
            data.name = form.cleaned_data['name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.pincode = form.cleaned_data['pincode']
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
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'grand_total':grand_total,
                'discount':discount
            }
            return render(request, 'store/payment.html',context)
        else:
            return redirect('checkout')
    else:
        return redirect('checkout')

            

            
            
def payment(request,method,order_number):
    
    if method == 'COD':
        order = Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
        payment = Payment(
            user=request.user,
            payment_id='PID-COD'+order_number,
            payment_method=method,
            amount_paid=order.order_total,
            payment_status='SUCCESS',
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        
        #move cart items to order product table
        cart_items = CartItem.objects.filter(user=request.user)
        
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
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
        
        request.session["order_number"] = order_number
        request.session["payment_id"] = 'PID-COD'+order_number
        return redirect('order_complete')
    
def order_complete(request):
    try: 
        if(request.session['order_number'] and request.session["payment_id"]):
            order_number= request.session['order_number']  
            payment_id=request.session['payment_id']
            
            try:
                order = Order.objects.get(order_number=order_number,is_ordered=True)
                ordered_products = OrderProduct.objects.filter(order_id=order.id)
                sub_total = 0
                for i in ordered_products:
                    sub_total += i.product_price * i.quantity
                payment = Payment.objects.get(payment_id=payment_id)
                context = {
                    'order':order,
                    'order_number':order_number,
                    'payment':payment,
                    'sub_total':sub_total,
                    'ordered_products':ordered_products
                }
                del request.session['order_number']
                del request.session['payment_id']
                return render(request, 'store/order_complete.html',context)
            except Exception:
                return redirect('home')
            
                
    except:
        return redirect('home')
    
    
    
def order_cancel_user(request,order_id):
    order = Order.objects.get(user=request.user,order_number=order_id)
    order.order_status='Cancelled_User'
    order.save()
    
    return redirect('order-history-detail',order_id=order.order_number)
    
    
    
    
#ADMIN  SIDE ORDER MANAGEMENT

def all_orders_admin(request):
    orders = Order.objects.all().order_by('-created_at')
    context={
        'orders':orders
    }
    return render(request, 'admincontrol/all_orders.html',context)


def admin_order_history_detail(request,order_id):
    order = Order.objects.get(order_number=order_id)
    order_products = OrderProduct.objects.filter(order=order)
    payment = Payment.objects.get(payment_id=order.payment)
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
            return JsonResponse({"status": "success"})
        except Order.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Order Not Found"})
        # Return a JSON response indicating success or failure
        
    else:
        # Return a JSON response indicating an invalid request
        return JsonResponse({"status": "error", "message": "Invalid request"})
    