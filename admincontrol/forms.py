from django.forms import ModelForm
from accounts.models import User


class CreateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","phone_number","password","email","is_superuser","is_active","is_email_verified","is_staff"]
        
class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","phone_number","email","is_superuser","is_active","last_name","is_email_verified","is_staff"]
        