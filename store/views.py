from django.shortcuts import render,get_object_or_404,redirect
from product_management.models import Product_Variant
from categoryManagement.models import Category
# Create your views here.


def home (request):
    return render(request, 'store/home.html')

def store (request,category_slug=None):
    categories = None
    product_variants = None
    
    if category_slug !=None:
        category = get_object_or_404(Category,cat_slug=category_slug)
        product_variants = Product_Variant.objects.select_related('product').prefetch_related('atributes').filter(product__product_catg=category,is_active=True)
        product_variants_count = product_variants.count()
    else:
        product_variants = Product_Variant.objects.select_related('product').prefetch_related('atributes').filter(is_active=True)
        product_variants_count = product_variants.count()
    context = {'product_variants':product_variants,
               'product_variants_count':product_variants_count}
    return render(request, 'store/store.html',context)

def product_variant_detail(request,category_slug,product_variant_slug):
    single_product_variant=None
    try:
        single_product_variant = Product_Variant.objects.select_related('product').prefetch_related('atributes','additional_product_images').get(
                            product__product_catg__cat_slug=category_slug,
                            product_variant_slug=product_variant_slug,
                            is_active=True)
    except Exception as e:
        print(e)
        return redirect('store')
    
    product_variants = Product_Variant.objects.filter(product=single_product_variant.product)
    product_variants_count=product_variants.count()
   
    
    context = { 'single_product_variant' :single_product_variant,
               'product_variants':product_variants,
               'product_variants_count':product_variants_count}
    
    return render(request, 'store/product_variant_detail.html',context)

