from product_management.models import Brand
# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
def all_category(request):
    
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, 'admincontrol/all_category.html',context)

