from django.forms import ModelForm
from accounts.models import User,AdressBook

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "password", "phone_number"]
    
class AdressBookForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
    class Meta:
        model = AdressBook
        exclude = ('user','is_default','is_active')

    