from django.contrib import admin
from django.contrib.admin.sites import site

from .models import Bill, BillProduct, Customer, Order, OrderProduct, Product, Rate, Staff, StaffWork, User



class CustomerDisplay(admin.ModelAdmin):
    list_display = ('customerId', 'name', 'address', 'phone', 'email')



class RateDisplay(admin.ModelAdmin):
    list_display = ('rateId', 'date', 'hallmarkRate', 'tajabiRate', 'silverRate')



class BillDisplay(admin.ModelAdmin):
    list_display = ('billId', 'customerId', 'orderId', 'date', 'rate', 'billType', 'customerProductWeight', 'customerProductAmount', 'finalWeight', 'grandTotalWeight', 'totalAmount', 'discount', 'grandTotalAmount', 'advanceAmount', 'payedAmount', 'remainingAmount', 'status', 'qr_code')



class OrderDisplay(admin.ModelAdmin):
    list_display = ('orderId', 'customerId', 'date', 'type', 'rate', 'customerProductWeight', 'advanceAmount', 'submittionDate', 'submittedDate', 'status', 'remark')



class ProductDisplay(admin.ModelAdmin):
    list_display = ('productId', 'productName', 'netWeight', 'size', 'gemsName', 'gemsPrice')



class BillProductDisplay(admin.ModelAdmin):
    list_display = ('billProductId', 'billId', 'productId', 'quantity', 'lossWeight', 'totalWeight', 'rate', 'makingCharge', 'totalAmountPerProduct',)



class OrderProductDisplay(admin.ModelAdmin):
    list_display = ('orderProductId', 'orderId', 'productId', 'totalWeight', 'quantity', 'design','status')



class StaffDisplay(admin.ModelAdmin):
    list_display = ('staffId',  'staffName', 'address', 'phone', 'email', 'registrationDate', 'resignDate') 



class StaffWorkDisplay(admin.ModelAdmin):
    list_display = ('staffWorkId', 'staff', 'orderProduct', 'date', 'givenWeight', 'KDMWeight', 'totalWeight',  'submittionDate', 'submittedWeight', 'finalProductWeight', 'lossWeight', 'submittedDate', 'status')


class UserDisplay(admin.ModelAdmin):
    list_display = ('id', 'username', 'full_name',  'first_name', 'last_name', 'email', 'phone', 'register_date', 'pan_number')




# Register your models here.
admin.site.register(User,UserDisplay)
admin.site.register(Customer, CustomerDisplay)
admin.site.register(Rate, RateDisplay)
admin.site.register(Bill, BillDisplay)
admin.site.register(Order, OrderDisplay)
admin.site.register(Product, ProductDisplay)
admin.site.register(BillProduct, BillProductDisplay)
admin.site.register(OrderProduct, OrderProductDisplay)
admin.site.register(Staff, StaffDisplay)
admin.site.register(StaffWork, StaffWorkDisplay)