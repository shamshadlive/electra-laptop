from django.forms import ModelForm
from django import forms

from .models import CategoryOffer,ProductOffer
from store.models import Banner

class DateInput(forms.DateInput):
    input_type = 'date'
class CreateCategoryOfferForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['is_active'].widget.attrs['class'] = ''    
    class Meta:
        model = CategoryOffer
        fields = '__all__'
        exclude = ['category_offer_slug']
        widgets = {
            'expire_date': DateInput(),
        }
        
class CreateProductOfferForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['is_active'].widget.attrs['class'] = ''    
    class Meta:
        model = ProductOffer
        fields = '__all__'
        exclude = ['product_offer_slug']
        widgets = {
            'expire_date': DateInput(),
        }
        
        
        
class CreateBannerForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['is_active'].widget.attrs['class'] = ''    
    class Meta:
        model = Banner
        fields = '__all__'
        # exclude = ['category_offer_slug']
        # widgets = {
        #     'expire_date': DateInput(),
        # }