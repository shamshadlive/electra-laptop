from django.forms import ModelForm
from .models import Category


class CreateCategoryForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        self.fields['parent_cat'].widget.attrs['class'] = 'form-control'
      
        
        
    class Meta:
        model = Category
        fields = ["cat_name","parent_cat","is_active"]
        
class EditCategoryForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        self.fields['parent_cat'].widget.attrs['class'] = 'form-control'
    class Meta:
        model = Category
        fields = ["cat_name","parent_cat","cat_slug","is_active"]
        
        