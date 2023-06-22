from django.shortcuts import render

# Create your views here.

def loginpage (request):
    return render(request, 'accounts/userlogin.html')

