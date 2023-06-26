
from .models import Category
# Create your views here.
from .forms import CreateCategoryForm,EditCategoryForm
from django.shortcuts import render,redirect
from django.contrib import messages
def all_category(request):
    
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, 'admincontrol/all_category.html',context)


def create_category(request):
    
    form = CreateCategoryForm()
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Created ")
            return redirect('admin-all-category')
        else:
            context = {'form':form}
            return render(request, 'admincontrol/category-create.html',context)
        
    context = {'form':form}
    return render(request, 'admincontrol/category-create.html',context)
    

def edit_category(request,cat_slug):
    
    try:
        category = Category.objects.get(cat_slug=cat_slug)
    except Category.DoesNotExist:
        return redirect('admin-all-category')
    except ValueError:
        return redirect('admin-all-category')

    form = EditCategoryForm(instance=category)
    
    if request.method == 'POST':
        form = EditCategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated")
            return redirect('admin-category-edit',cat_slug)
        else:
            messages.error(request, form.errors)
            return render(request, 'admincontrol/category-edit.html', {'form': form,'cat_slug':cat_slug})
    context = {'form':form,'cat_slug':cat_slug}
    return render(request, 'admincontrol/category-edit.html',context)
    
    
    
    
    

def delete_category(request,cat_slug):
    
    try:
        category = Category.objects.get(cat_slug=cat_slug)
    except User.DoesNotExist:
        return redirect('admin-all-category')
    except ValueError:
        return redirect('admin-all-category')
    category.delete()
    messages.error(request, "Category Deleted ❌")
    return redirect('admin-all-category')
   
    
    
    
    