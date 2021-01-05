from django.contrib import admin
from django.contrib.auth.models import User

# from extra_apps import xadmin
from .models import Customer, Commodity, Staff, Order, Order_detail, Shipping_address, Shopping_cart_details, Sales
# # Register your models here.
admin.site.register(Customer)
# admin.site.register(Commodity)
admin.site.register(Staff)
admin.site.register(Order)
admin.site.register(Order_detail)
admin.site.register(Shipping_address)
admin.site.register(Shopping_cart_details)
admin.site.register(Sales)

@admin.register(Commodity)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['upload_img']
    list_display = ("name", "purchase_price", "selling_price", "sales", "stock")


