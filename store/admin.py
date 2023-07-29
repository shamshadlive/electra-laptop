from django.contrib import admin
from .models import Banner,ReviewRating,RecentViewedProduct
# Register your models here.

admin.site.register(Banner)
admin.site.register(ReviewRating)
admin.site.register(RecentViewedProduct)