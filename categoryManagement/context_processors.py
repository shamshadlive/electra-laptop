 
from .models import Category

def all_category(request):
     all_category_list = Category.objects.filter(is_active=True)
     return dict(all_category_list=all_category_list) 