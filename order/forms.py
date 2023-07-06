from django import forms
from .models import Order



# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['name','phone','email','address_line_1','address_line_2','country','state','city','order_note','pincode']
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_note']
    
class ChangeOrderStatusForm(forms.ModelForm):

   class Meta:
         model = Order
         fields = ['order_status']