from django.contrib import admin
from .models import Order,OrderProduct,Payment,PaymentMethod
# Register your models here.



class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields =['user','product','product_price']


class OrderAdmin(admin.ModelAdmin):
    # list_display = ['order_number','name','order_total','is_ordered','created_at']
    list_filter = ['is_ordered']
    # search_fields = ['order_number','name','email']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)
admin.site.register(PaymentMethod)