from product_management.models import Brand,Atribute,Atribute_Value
# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import CreateBrandForm,CreateAtributeForm,CreateAtributeValueForm



#===========BRAND MANAGEMENT==================
def all_brand(request):
    
    brands = Brand.objects.all()
    context = {
        'brands':brands
    }
    return render(request, 'admincontrol/all_brand.html',context)


def create_brand(request):
    
    form = CreateBrandForm()
    if request.method == 'POST':
        form = CreateBrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Brand Created ")
            return redirect('admin-all-brand')
        else:
            context = {'form':form}
            return render(request, 'admincontrol/brand-create.html',context)
        
    context = {'form':form}
    return render(request, 'admincontrol/brand-create.html',context)
    

#===========ATRIBUTE MANAGEMENT==================

def all_atribute(request):
    
    atributes = Atribute.objects.all()
    context = {
        'atributes':atributes
    }
    return render(request, 'admincontrol/all_atribute.html',context)


def create_atribute(request):
    
    form = CreateAtributeForm()
    if request.method == 'POST':
        form = CreateAtributeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Atibute Created ")
            return redirect('admin-all-atribute')
        else:
            context = {'form':form}
            return render(request, 'admincontrol/atribute-create.html',context)
        
    context = {'form':form}
    return render(request, 'admincontrol/atribute-create.html',context)
    

#===========ATRIBUTE VALUE MANAGEMENT==================

def all_atribute_value(request):
    
    atribute_values = Atribute_Value.objects.all()
    context = {
        'atribute_values':atribute_values
    }
    return render(request, 'admincontrol/all_atribute_value.html',context)


def create_atribute_value(request):
    
    form = CreateAtributeValueForm()
    if request.method == 'POST':
        form = CreateAtributeValueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Atribute Value Created ")
            return redirect('admin-all-atribute_value')
        else:
            context = {'form':form}
            return render(request, 'admincontrol/atribute_value-create.html',context)
        
    context = {'form':form}
    return render(request, 'admincontrol/atribute_value_create.html',context)
    
