from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import Wallet
from order.models import Order
# Create your views here.

def get_wallet_grand_total(request):
    
    order_number = request.GET.get('order_number')
    check = request.GET.get('check')
    if order_number:
        
        wallet = Wallet.objects.get(user=request.user,is_active=True)
        order = Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
        grand_total = order.order_total
        wallet_balance = wallet.balance  
        
        if check=='true':  
            if wallet.balance <= grand_total  :  
                grand_total = grand_total- wallet.balance   
                wallet_balance = 0
            else:
                wallet_balance = wallet.balance - grand_total
                grand_total = 0
                    
            return JsonResponse({"status": "success", "grand_total":grand_total,"wallet_balance":wallet_balance})
        else:
            return JsonResponse({"status": "success", "grand_total":grand_total,"wallet_balance":wallet_balance})
            
    