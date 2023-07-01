from product_management.models import Brand
# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import CreateBrandForm



#BRAND MANAGEMENT
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
    