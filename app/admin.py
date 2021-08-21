from django.contrib import admin
from . models import (
    Customer,
    Cart,
    Product,
    OrderPlaced
)

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [ 'id','user','name','locality','city','pincode','states' ]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'id','title' ,'selling_price','discounted_price','description'
    ,'brand','category','product_img']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [ 'id','user','product','quantity'  ]    


@admin.register(OrderPlaced)
class OrderPalcedAdmin(admin.ModelAdmin):
    list_display = [ 'id','user','cutomer','product','quantity', 'ordered_date', 'status' ]