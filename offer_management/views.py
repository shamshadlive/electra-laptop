from django.shortcuts import render,redirect
from django.views.generic.list import ListView  
from .models import CategoryOffer,ProductOffer
from datetime import datetime
from product_management.models import Product_Variant
from django.shortcuts import get_object_or_404
from django.views.generic import View
from categoryManagement.models import Category
from cart.models import Wishlist,WishlistItem
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator 
from django.urls import path, reverse_lazy
from .forms import CreateCategoryOfferForm,CreateBannerForm,CreateProductOfferForm
from django.views.generic.edit import CreateView, UpdateView ,DeleteView  
 
from store.models import Banner
# Create your views here.



class all_offers_store(ListView):  
    model = CategoryOffer  
    template_name = 'store/all_offers.html'
    context_object_name = 'categoryOffers'
  
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset=CategoryOffer.objects.filter(is_active=True, expire_date__gte=datetime.now()) 
       
        return queryset


class category_offer_product(View):
    def get(self, request, offer_slug, category=None):

        price_min = request.GET.get('price-min')
        price_max = request.GET.get('price-max')
        
        #wishlist
        if request.user.is_authenticated:  
            wishlist,created= Wishlist.objects.get_or_create(user=request.user)
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True).values_list('product_id', flat=True)
        else:
            wishlist_items =[]
            
    
        try:
            category_offer = get_object_or_404(CategoryOffer, category_offer_slug=offer_slug)
        except:
            return redirect('store')
    
        categories = category_offer.category.filter(is_active=True)
        
        if category:
            category = category_offer.category.filter(is_active=True,cat_slug=category)
            product_variants = Product_Variant.objects.select_related('product').prefetch_related('atributes').filter(product__product_catg__in=category,is_active=True)
            product_variants_count = product_variants.count()
        else:
            product_variants = Product_Variant.objects.select_related('product').prefetch_related('atributes').filter(product__product_catg__in=categories,is_active=True)
            product_variants_count = product_variants.count()
        
        #price filter 
        if price_min:
            product_variants = product_variants.filter(sale_price__gte=price_min)
        if price_max:
            product_variants = product_variants.filter(sale_price__lte=price_max)
            
            
        # Get all attribute names from the request avoid certain parameters
        attribute_names = [key for key in request.GET.keys() if key not in ['query','page','price-min','price-max']]
        
            #other filter
        for attribute_name in attribute_names:
            attribute_values = request.GET.getlist(attribute_name)
            if attribute_values:
                product_variants=product_variants.filter(atributes__atribute_value__in=attribute_values)
        
        product_variants_count = product_variants.count()
        
    
        # paginator start
        paginator = Paginator(product_variants,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        
            
        context = {
            'category_offer':category_offer,
                'product_variants':paged_products,
                'product_variants_count':product_variants_count,
                'all_category_list':categories,
                'price_min':price_min,
               'price_max':price_max,
               'wishlist_items':wishlist_items
                
            }
        return render(request,'store/offer_items.html',context)
    
    
    
    
    
    
    

#======admin offer management============

class admin_all_category_offer(ListView):  
    model = CategoryOffer  
    template_name = 'admincontrol/all_category_offer.html'
    context_object_name = 'categoryOffers'
  

class adminCategoryOfferCreate(CreateView):  
    model = CategoryOffer  
    template_name = 'admincontrol/category_offer_create.html'
    form_class = CreateCategoryOfferForm
    success_url = reverse_lazy('admin-all-category-offer')
    


class adminCategoryOfferUpdate(UpdateView):  
    model = CategoryOffer  
    template_name = 'admincontrol/category_offer_update.html'
    form_class = CreateCategoryOfferForm
    success_url = reverse_lazy('admin-all-category-offer')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_offer_id'] = self.kwargs['pk']
        return context

class adminCategoryOfferDelete(DeleteView):  
    model = CategoryOffer   
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete() 
        return redirect ('admin-all-category-offer')




#admin - product -offer managmenet

class admin_all_product_offer(ListView):  
    model = ProductOffer  
    template_name = 'admincontrol/all_product_offer.html'
    context_object_name = 'productOffers'
  

class adminProductOfferCreate(CreateView):  
    model = ProductOffer  
    template_name = 'admincontrol/product_offer_create.html'
    form_class = CreateProductOfferForm
    success_url = reverse_lazy('admin-all-product-offer')
    


class adminProductOfferUpdate(UpdateView):  
    model = ProductOffer  
    template_name = 'admincontrol/product_offer_update.html'
    form_class = CreateProductOfferForm
    success_url = reverse_lazy('admin-all-product-offer')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_offer_id'] = self.kwargs['pk']
        return context

class adminProductOfferDelete(DeleteView):  
    model = ProductOffer   
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete() 
        return redirect ('admin-all-product-offer')















#admin banner managment

class admin_all_banner(ListView):  
    model = Banner 
    template_name = 'admincontrol/all_banner.html'
    context_object_name = 'banners'
  

class adminBannerCreate(CreateView):  
    model = Banner  
    template_name = 'admincontrol/banner_create.html'
    form_class = CreateBannerForm
    success_url = reverse_lazy('admin-all-banner')
    


class adminBannerUpdate(UpdateView):  
    model = Banner  
    template_name = 'admincontrol/banner_update.html'
    form_class = CreateBannerForm
    success_url = reverse_lazy('admin-all-banner')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banner_id'] = self.kwargs['pk']
        return context
    

class adminBannerDelete(DeleteView):  
    model = Banner
    success_url = reverse_lazy('admin-all-banner')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete() 
        return redirect ('admin-all-banner')