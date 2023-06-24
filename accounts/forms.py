from django.forms import ModelForm
from accounts.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "password", "phone_number"]
    