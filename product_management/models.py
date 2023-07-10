from django.db import models
from categoryManagement.models import Category
from django.utils.text import slugify
from django.db.models import UniqueConstraint, Q,F
from collections import defaultdict
from django.urls import reverse
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


    def get_url(self):
        return reverse('product-variant-detail',args=[self.product.product_catg.cat_slug,self.product_variant_slug])
    
    def get_product_name(self):
        return f'{self.product.product_brand} {self.product.product_name}-{self.sku_id}'
    
    def __str__(self):
        return f'{self.sku_id} - {self.atributes.values("atribute_value")}'
         

# FOR ADDITIONAL IMAGES
class Additional_Product_Image(models.Model):
    product_variant = models.ForeignKey(Product_Variant,on_delete=models.CASCADE,related_name='additional_product_images')
    image = models.ImageField(upload_to='product_variant/additional/images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.image.url
    