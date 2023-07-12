 
from .models import Category
from product_management.models import Atribute

def all_category(request):
     all_category_list = Category.objects.filter(is_active=True)
     return dict(all_category_list=all_category_list) 

def all_atribute(request):
     all_atribute_list = Atribute.objects.filter(is_active=True)
     return dict(all_atribute_list=all_atribute_list) 