from django.contrib import admin
from .models import *
class OrderProductInline(admin.TabularInline):
    model=Order_product
    readonly_fields=('user','payment','product','quantity','ordered','product_price')
    extra=0
class OrderAdmin(admin.ModelAdmin):
    list_display=['order_number','first_name','last_name','phone_number','email','city','order_total','tax','status','is_orderd','created_at']
    list_filter=['status','is_orderd']
    search_fields=['order_number','first_name','last_name','phone_number','email']
    list_per_page=20
    inlines=[OrderProductInline]
class ContactAdmin(admin.ModelAdmin):
    list_display=['name','phone','email','subject','message']
    list_per_page=20
    readonly_fields=('name','phone','email','subject','message')
admin.site.register(Catagory)
# admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order,OrderAdmin)
admin.site.register(Order_product)
admin.site.register(Contact_mod,ContactAdmin)
admin.site.register(Cart)
admin.site.register(Cart_item)
admin.site.register(Payment)
# admin.site.register(Shiping_adress)
# Register your models here. 
