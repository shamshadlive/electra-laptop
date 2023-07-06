from django.db import models
from accounts.models import User,AdressBook
from product_management.models import Product_Variant

# Create your models here.
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES =(
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Success"),
        )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
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
        ("Cancelled_Admin", "Cancelled_Admin"),
        ("Cancelled_User", "Cancelled_User"),
        )
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    order_number = models.CharField(max_length=100)
    shipping_address = models.ForeignKey(AdressBook,on_delete=models.SET_NULL,null=True)
    #address later updated to adress table
    # name = models.CharField(max_length=30)
    # phone = models.CharField(max_length=20)
    # email = models.EmailField(max_length=50)
    # address_line_1 = models.CharField(max_length=50)
    # address_line_2 = models.CharField(max_length=50,blank=True,null=True)
    # country = models.CharField(max_length=50)
    # state = models.CharField(max_length=50)
    # city = models.CharField(max_length=50)
    # pincode = models.CharField(max_length=20)
    
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
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product_Variant,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=12, decimal_places=2)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.order)