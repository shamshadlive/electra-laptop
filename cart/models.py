from django.db import models
from product_management.models import Product_Variant 
from accounts.models import User
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
    
    
    def sub_total(self):
        return self.product.sale_price * self.quantity
    
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
    
    def __str__(self):
        return str(self.product)
    
    