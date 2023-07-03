from django.forms import ModelForm
from product_management.models import Brand,Atribute,Atribute_Value


class CreateBrandForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
    class Meta:
        model = Brand
        fields = '__all__'
 
class CreateAtributeForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
    class Meta:
        model = Atribute
        fields = '__all__'
 
class CreateAtributeValueForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['is_active'].widget.attrs['class'] = ''
           
    class Meta:
        model = Atribute_Value
        fields = '__all__'