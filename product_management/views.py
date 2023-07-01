from django.shortcuts import render

# Create your views here.
from .models import Product,Product_Variant,Atribute,Atribute_Value,Additional_Product_Image
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .forms import EditProductForm,EditProductVariantForm,CreateProductForm,CreateProductVariantForm,AddProductVariantForm









# ====================PRODUCT MAANGEMENT ===============
def all_product(request):
    
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request, 'admincontrol/all_products.html',context)



def edit_product(request,product_slug):
    try:
        product = Product.objects.get(product_slug=product_slug) 
        product_variants=Product_Variant.objects.filter(product=product)
    except Product.DoesNotExist:
        return redirect('admin-all-product')
    except ValueError:
        return redirect('admin-all-product')

    product_form = EditProductForm(instance=product)
    
    if request.method == 'POST':
        product_form = EditProductForm(request.POST,instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "product Updated")
            return redirect('admin-product-edit',product_slug)
        else:
            messages.error(request, product_form.errors)
            return render(request, 'admincontrol/product-edit.html', {'product_form': product_form,
                                                                      'product_variants':product_variants,
                                                                      'product_slug':product_slug})
    context = {'product_form': product_form,
               'product_variants':product_variants,
                # 'product_variant_form':product_variant_form,
                'product_slug':product_slug}
    return render(request, 'admincontrol/product-edit.html',context)



def delete_product(request,product_slug):
    
    try:
        product = Product.objects.get(product_slug=product_slug)
    except Product.DoesNotExist:
        return redirect('admin-all-product')
    except ValueError:
        return redirect('admin-all-product')
    product.delete()
    messages.error(request, "product Deleted ❌")
    return redirect('admin-all-product')
   
    
    
# ====================PRODUCT VARIANT ===============
# create_product_with_variant

def create_product_with_variant(request):
    #getting all atributes and atributes  value
    attributes = Atribute.objects.prefetch_related('atribute_value_set').filter(is_active=True)
    
    attribute_dict = {}
    for attribute in attributes:
        attribute_values = attribute.atribute_value_set.filter(is_active=True)
        attribute_dict[attribute.atribute_name] = attribute_values
    #to show how many atribute in fronend
    attribute_values_count = attributes.count() 
    if request.method == 'POST':
        product_form = CreateProductForm(request.POST)
        variant_form = CreateProductVariantForm(request.POST, request.FILES)
        attribute_ids=[]
        #getting all atributes
        for i in range(1,attribute_values_count+1):
            req_atri = request.POST.get('atributes_'+str(i))
            if req_atri != 'None':
                attribute_ids.append(int(req_atri))
    
        product = product_form.save()
        variant = variant_form.save(commit=False)
        variant.product = product
        variant.save()
        variant.atributes.set(attribute_ids) # Save ManyToManyField relationships
        additional_images = request.FILES.getlist('additional_images')
        additional_images_id =[]
        for image in additional_images:
            created = Additional_Product_Image.objects.create(image=image)
            additional_images_id.append(created.id)
        
        variant.additional_images.set(additional_images_id)
        print("==========================")
        print(additional_images)
        print(additional_images_id)
        
        return redirect('admin-all-product')
        
    else:
        product_form = CreateProductForm()
        variant_form = CreateProductVariantForm()
    
    return render(request, 'admincontrol/product-create.html', {'product_form': product_form, 
                                                                'variant_form': variant_form,
                                                                'attribute_dict':attribute_dict
                                                                })




def add_product_variant(request,product_slug):
    
    try:
        product = Product.objects.get(product_slug=product_slug) 
    except Product.DoesNotExist:
        return redirect('admin-all-product')
    except ValueError:
        return redirect('admin-all-product')

    add_product_variant_form = AddProductVariantForm(initial={'product': product})
    attributes = Atribute.objects.prefetch_related('atribute_value_set').filter(is_active=True)
    
    attribute_dict = {}
    for attribute in attributes:
        attribute_values = attribute.atribute_value_set.filter(is_active=True)
        attribute_dict[attribute.atribute_name] = attribute_values
    #to show how many atribute in fronend
    attribute_values_count = attributes.count() 
    
    
    if request.method == 'POST':
        add_product_variant_form = AddProductVariantForm(request.POST, request.FILES,initial={'product': product})
        attribute_ids=[]
        #getting all atributes
        for i in range(1,attribute_values_count+1):
            req_atri = request.POST.get('atributes_'+str(i))
            if req_atri != 'None':
                attribute_ids.append(int(req_atri))
        if add_product_variant_form.is_valid():
            variant = add_product_variant_form.save()
            variant.atributes.set(attribute_ids)    # Save ManyToManyField relationships
            variant.save()
            additional_images = request.FILES.getlist('additional_images')
            additional_images_id =[]
            for image in additional_images:
                created = Additional_Product_Image.objects.create(image=image)
                additional_images_id.append(created.id)
        
            variant.additional_images.set(additional_images_id)
            messages.success(request, "Variant Created")
            return redirect('admin-product-edit',product_slug)
    context = {'add_product_variant_form': add_product_variant_form,
               'product_slug':product_slug,
               'attribute_dict':attribute_dict
               }
    return render(request, 'admincontrol/product-variant-create.html',context)


    





def edit_product_variant(request,product_variant_slug):
    try:
        product_variant = Product_Variant.objects.get(product_variant_slug=product_variant_slug) 
    except Product_Variant.DoesNotExist:
        return redirect('admin-all-product')
    except ValueError:
        return redirect('admin-all-product')

    product_variant_form = EditProductVariantForm(instance=product_variant)
    
    if request.method == 'POST':
        product_variant_form = EditProductVariantForm(request.POST, request.FILES,instance=product_variant)
        if product_variant_form.is_valid():
            product_variant_form.save()
            messages.success(request, "Variant Updated")
            return redirect('admin-product-variant-edit',product_variant_slug)
        else:
            messages.error(request, product_variant_form.errors)
            return render(request, 'admincontrol/product-variant-edit.html', {'product_variant_form': product_variant_form,
                                                                      
                                                                    #   'product_variant_form':product_variant_form,
                                                                      'product_variant_slug':product_variant_slug})
    context = {'product_variant_form': product_variant_form,
                'product_variant_slug':product_variant_slug}
    return render(request, 'admincontrol/product-variant-edit.html',context)



def delete_product_variant(request,product_variant_slug):
    
    try:
        product_variant = Product_Variant.objects.get(product_variant_slug=product_variant_slug)
    except Product_Variant.DoesNotExist:
        return redirect('admin-all-product')
    except ValueError:
        return redirect('admin-all-product')
    product_variant.delete()
    messages.error(request, "Variant Deleted ❌")
    return redirect('admin-all-product')
   
    