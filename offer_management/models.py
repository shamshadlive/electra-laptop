from django.db import models
from categoryManagement.models import Category
from django.utils.text import slugify
from product_management.models import Product_Variant
# Create your models here.

class CategoryOffer(models.Model):
    offer_name = models.CharField(max_length=100)
    expire_date = models.DateField()
    category = models.ManyToManyField(Category)
    discount_percentage = models.IntegerField(default=0)
    category_offer_slug = models.SlugField( blank=True,max_length=200,unique=True)
    category_offer_image = models.ImageField(upload_to='category_offer/images/')
    is_active = models.BooleanField(default=True)
    
    
    def save(self, *args, **kwargs):
        if self.discount_percentage > 100:
            self.discount_percentage = 100
            
        counter = CategoryOffer.objects.filter(category_offer_slug__startswith=self.category_offer_slug).count()
        if counter > 0:
            self.category_offer_slug = slugify(f'{self.offer_name}-{counter}')
        else:
            self.category_offer_slug =slugify(self.offer_name) 
        
        super(CategoryOffer, self).save(*args, **kwargs)

    def __str__(self):
        return self.offer_name


class ProductOffer(models.Model):
    offer_name = models.CharField(max_length=100)
    expire_date = models.DateField()
    product = models.ManyToManyField(Product_Variant)
    discount_percentage = models.IntegerField(default=0)
    product_offer_slug = models.SlugField( blank=True,max_length=200,unique=True)
    product_offer_image = models.ImageField(upload_to='product_offer/images/')
    is_active = models.BooleanField(default=True)
    
    
    def save(self, *args, **kwargs):
        if self.discount_percentage > 100:
            self.discount_percentage = 100
            
        counter = ProductOffer.objects.filter(product_offer_slug__startswith=self.product_offer_slug).count()
        if counter > 0:
            self.product_offer_slug = slugify(f'{self.offer_name}-{counter}')
        else:
            self.product_offer_slug =slugify(self.offer_name) 
        
        super(ProductOffer, self).save(*args, **kwargs)

    def __str__(self):
        return self.offer_name

