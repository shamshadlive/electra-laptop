from django.db import models
from  product_management.models import Product_Variant
from accounts.models import User
# Create your models here.


class Banner(models.Model):
    banner_name = models.CharField(max_length=100)
    banner_image = models.ImageField(upload_to='banner/images/')
    banner_url = models.URLField(blank=True,null=True)
    button_text = models.CharField(max_length=10,default='Buy Now')
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.banner_name

# REVIEW AND RATING MODEL
class ReviewRating(models.Model):
    product = models.ForeignKey(Product_Variant,on_delete=models.CASCADE , related_name='product_review')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100,blank=True )
    review = models.TextField(max_length=500,blank=True )
    rating = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject

