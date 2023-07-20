from django.db import models
from product_management.models import Product_Variant 
from accounts.models import User
from datetime import datetime
# Create your models here.

class Cart(models.Model):
    
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product_Variant,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    
    # def sub_total(self):
    #     return self.product.sale_price * self.quantity
    def sub_total(self):
       
            
        offer_percentage=0
        #adding catggry offer
        if self.product.product.product_catg.categoryoffer_set.filter(is_active=True, expire_date__gte=datetime.now()).exists():
                offer_percentage = self.product.product.product_catg.categoryoffer_set.filter(is_active=True, expire_date__gte=datetime.now()).values_list('discount_percentage', flat=True).order_by('-discount_percentage').first()
        
        #adding product offer
        if self.product.productoffer_set.filter(is_active=True, expire_date__gte=datetime.now()).exists():
                offer_percentage = offer_percentage+self.product.productoffer_set.filter(is_active=True, expire_date__gte=datetime.now()).values_list('discount_percentage', flat=True).order_by('-discount_percentage').first()

        if offer_percentage >=100:
            offer_percentage = 100
            
        offer_price =  self.product.sale_price - self.product.sale_price * (offer_percentage) / (100)
        
        return offer_price * self.quantity
        
    
    def __str__(self):
        return str(self.product)
    
    
class Wishlist(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return str(self.user)

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE)
    product = models.ForeignKey(Product_Variant,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.product)
    
    