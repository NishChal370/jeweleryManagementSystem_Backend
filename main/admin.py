from django.contrib import admin
from django.contrib.admin.sites import site

from .models import Bill, BillProduct, Customer, Order, OrderProduct, Product, Rate

class CustomerDisplay(admin.ModelAdmin):
    list_display = ('customerId', 'name', 'address', 'phone', 'email')



class RateDisplay(admin.ModelAdmin):
    list_display = ('rateId', 'date', 'hallmarkRate', 'tajabiRate', 'silverRate')



class BillDisplay(admin.ModelAdmin):
    list_display = ('billId', 'customerId', 'orderId', 'date', 'rate', 'customerProductWeight', 'customerProductAmount', 'totalAmount', 'discount', 'grandTotalAmount', 'advanceAmount', 'payedAmount', 'remainingAmount', 'status')

class OrderDisplay(admin.ModelAdmin):
    list_display = ('orderId', 'customerId', 'date', 'rate', 'advanceAmount', 'submittionDate', 'submittedDate', 'design', 'status', 'remark')

class ProductDisplay(admin.ModelAdmin):
    list_display = ('productId', 'productName', 'netWeight', 'size', 'gemsName', 'gemsPrice')

class BillProductDisplay(admin.ModelAdmin):
    list_display = ('billProductId', 'billId', 'productId', 'lossWeight', 'totalWeight', 'rate', 'makingCharge', 'totalAmountPerProduct')

class OrderProductDisplay(admin.ModelAdmin):
    list_display = ('orderProductId', 'orderId', 'productId', 'totalWeight', 'status')



# Register your models here.
admin.site.register(Customer, CustomerDisplay)
admin.site.register(Rate, RateDisplay)
admin.site.register(Bill, BillDisplay)
admin.site.register(Order, OrderDisplay)
admin.site.register(Product, ProductDisplay)
admin.site.register(BillProduct, BillProductDisplay)
admin.site.register(OrderProduct, OrderProductDisplay)