from django.db import models
from accounts.models import User,AdressBook
from product_management.models import Product_Variant,Coupon
from django.db.models.signals import post_save 
from django.dispatch import receiver
# Create your models here.
class PaymentMethod(models.Model):
    method_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.method_name




class Payment(models.Model):
    PAYMENT_STATUS_CHOICES =(
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Success"),
        )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    payment_order_id = models.CharField(max_length=100,null=True,blank=True)
    payment_signature = models.CharField(max_length=100,null=True,blank=True)
    payment_method = models.CharField(max_length=100,null=True,blank=True)
    amount_paid = models.CharField(max_length=30)
    payment_status= models.CharField(choices = PAYMENT_STATUS_CHOICES,max_length=20)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id

class Order(models.Model):
    ORDER_STATUS_CHOICES =(
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Delivered", "Delivered"),
        ("Cancelled_Admin", "Cancelled Admin"),
        ("Cancelled_User", "Cancelled User"),
        ("Returned_User", "Returned User"),
        )
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    order_number = models.CharField(max_length=100)
    shipping_address = models.ForeignKey(AdressBook,on_delete=models.SET_NULL,null=True)
    
    coupon_code = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    additional_discount = models.IntegerField(default=0,null=True)
    wallet_discount = models.IntegerField(default=0,null=True)
    order_note = models.CharField(max_length=100,blank=True,null=True)
    order_total = models.DecimalField(max_digits=12, decimal_places=2)
    order_status= models.CharField(choices = ORDER_STATUS_CHOICES,max_length=20,default='New')
    ip = models.CharField(max_length=50,blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.order_number


class OrderProduct(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product_Variant,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=12, decimal_places=2)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.order)


@receiver(post_save,sender=Payment)
def delete_unordered_orders(sender, instance , **kwargs):
    print("-----------")
    order = Order.objects.filter(user=instance.user,is_ordered=False).delete()
    pass