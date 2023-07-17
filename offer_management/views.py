from django.shortcuts import render

# Create your views here.



def all_offers_store (request):
    return render(request, 'store/all_offers.html')