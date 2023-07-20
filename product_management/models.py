from django.db import models
from categoryManagement.models import Category
from django.utils.text import slugify
from django.db.models import UniqueConstraint, Q,F,Avg,Count
from collections import defaultdict
from django.urls import reverse
from datetime import datetime
# Create your models here.

# Atribute Table - SYSTEM_MEMORY , INTERNAL_STORAGE , COLOR , INTERNAL_STORAGE_TYPE
class Atribute(models.Model):
    atribute_name = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.atribute_name
    
# Atribute Value - RED,BLUE, 4GB, 8GB, 128GB , SSD , HDD
class Atribute_Value(models.Model):
    atribute = models.ForeignKey(Atribute,on_delete=models.CASCADE)
    atribute_value = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.atribute_value+"-"+self.atribute.atribute_name
    
# Brand Table , ASUS , REALME , LENOVO , APPLE
class Brand(models.Model):
    brand_name = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name
     
   
         
# Product - MACBOOK PRO LIMITED EDITION
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_catg = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    product_brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    product_slug = models.SlugField(unique=True, blank=True,max_length=200)
    product_description = models.TextField(max_length=250)
    is_active = models.BooleanField(default=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    

    def save(self, *args, **kwargs):
        product_slug_name = f'{self.product_brand.brand_name}-{self.product_name}-{self.product_catg.cat_name}'
        base_slug = slugify(product_slug_name)
        counter = Product.objects.filter(product_slug__startswith=base_slug).count()
        if counter > 0:
            self.product_slug = f'{base_slug}-{counter}'
        else:
            self.product_slug = base_slug
        super(Product, self).save(*args, **kwargs)


    def __str__(self):
        return self.product_brand.brand_name+"-"+self.product_name 

class Product_VariantManager(models.Manager):
    """
    Custom manager
    """
    def get_all_variant(self,product):
        # variant = super(Product_VariantManager, self).get_queryset().filter(product=product).values('sku_id','atributes__atribute_value','atributes__atribute__atribute_name')
        variant = (
                    super(Product_VariantManager, self)
                    .get_queryset()
                    .filter(product=product)
                    .values('sku_id')
                    # .annotate(
                    #     atribute_value=F('atributes__atribute_value'),
                    #     atribute_name=F('atributes__atribute__atribute_name')
                    # )
                )
        return  variant



# Product - MACBOOK PRO LIMITED EDITION
class Product_Variant(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    sku_id = models.CharField(max_length=30)
    atributes = models.ManyToManyField(Atribute_Value,related_name='attributes')
    max_price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    product_variant_slug = models.SlugField(unique=True, blank=True,max_length=200)
    thumbnail_image = models.ImageField(upload_to='product_variant/images/')
    is_active = models.BooleanField(default=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    
    
    
    objects = models.Manager()
    variants = Product_VariantManager()
    
    
    def save(self, *args, **kwargs):
        product_variant_slug_name = f'{self.product.product_brand.brand_name}-{self.product.product_name}-{self.product.product_catg.cat_name}-{self.sku_id}'
        base_slug = slugify(product_variant_slug_name)
        counter = Product_Variant.objects.filter(product_variant_slug__startswith=base_slug).count()
        if counter > 0:
            self.product_variant_slug = f'{base_slug}-{counter}'
        else:
            self.product_variant_slug = base_slug
        super(Product_Variant, self).save(*args, **kwargs)

    
    class Meta:
        constraints = [
            UniqueConstraint(
                name='Unique skuid must be provided',
                fields=['product', 'sku_id'],
                condition=Q(sku_id__isnull=False),
            )
        ]

    def avrg_review(self):
        from store.models import ReviewRating    
        reviews = ReviewRating.objects.filter(product=self,is_active=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def count_review(self):
        from store.models import ReviewRating    
        reviews = ReviewRating.objects.filter(product=self,is_active=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def get_url(self):
        return reverse('product-variant-detail',args=[self.product.product_catg.cat_slug,self.product_variant_slug])
    
    def get_product_name(self):
        return f'{self.product.product_brand} {self.product.product_name}-{self.sku_id} - {", ".join([value[0] for value in self.atributes.all().values_list("atribute_value")])}'
    
    def product_price(self):
        offer_percentage=0
       
        #adding catggry offer
        if self.product.product_catg.categoryoffer_set.filter(is_active=True, expire_date__gte=datetime.now()).exists():
                offer_percentage = self.product.product_catg.categoryoffer_set.filter(is_active=True, expire_date__gte=datetime.now()).values_list('discount_percentage', flat=True).order_by('-discount_percentage').first()
        
        #adding product offer
        if self.productoffer_set.filter(is_active=True, expire_date__gte=datetime.now()).exists():
                offer_percentage = offer_percentage+self.productoffer_set.filter(is_active=True, expire_date__gte=datetime.now()).values_list('discount_percentage', flat=True).order_by('-discount_percentage').first()
        
        if offer_percentage >=100:
            offer_percentage = 100
         
        offer_price =  self.sale_price - self.sale_price * (offer_percentage) / (100)
        
        return offer_price 
        
        
    def product_offer(self):
        offer_price = {
            'offer_percentage': 0,
            'offer_name': ""
        }
        
        #category offer
        if self.product.product_catg.categoryoffer_set.filter(is_active=True, expire_date__gte=datetime.now()).exists():
            category_offer = self.product.product_catg.categoryoffer_set.filter(is_active=True, expire_date__gte=datetime.now()).order_by('-discount_percentage').first()
            offer_price['offer_percentage'] = category_offer.discount_percentage
            offer_price['offer_name'] = category_offer.offer_name
          
           
        #product_offer
        if self.productoffer_set.filter(is_active=True, expire_date__gte=datetime.now()).exists():
            try:
                product_offer = self.productoffer_set.filter(is_active=True, expire_date__gte=datetime.now()).order_by('-discount_percentage').first()
                
                offer_price['offer_percentage'] += product_offer.discount_percentage
                offer_price['offer_name'] += ","+product_offer.offer_name
            except Exception as e:
                
                print(e)
        if offer_price['offer_percentage'] >=100:
            offer_price['offer_percentage'] = 100
               
        return offer_price

    
    def __str__(self):
        return self.get_product_name()
         

# FOR ADDITIONAL IMAGES
class Additional_Product_Image(models.Model):
    product_variant = models.ForeignKey(Product_Variant,on_delete=models.CASCADE,related_name='additional_product_images')
    image = models.ImageField(upload_to='product_variant/additional/images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.image.url
    
    
#Coupons

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=10)
    minimum_amount = models.IntegerField(default=500)
    description = models.CharField(max_length=100)
    expire_date = models.DateField()
    
    
    
    def save(self, *args, **kwargs):
        if self.discount_percentage > 100:
            self.discount_percentage = 100
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.coupon_code