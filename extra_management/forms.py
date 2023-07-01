from django.forms import ModelForm
from product_management.models import Brand


class CreateBrandForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        
        
        
    class Meta:
        model = Brand
        fields = '__all__'
 