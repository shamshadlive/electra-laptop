from django.contrib import admin
from .models import User,UserOtp,AdressBook
# Register your models here.

admin.site.register(User)
admin.site.register(UserOtp)
admin.site.register(AdressBook)
