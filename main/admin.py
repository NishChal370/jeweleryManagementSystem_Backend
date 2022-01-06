from django.contrib import admin

from .models import Bill, Customer, Order

class CustomerDisplay(admin.ModelAdmin):
    list_display = ('customerId', 'name', 'address', 'phone', 'email')

class OrderDisplay(admin.ModelAdmin):
    list_display = ('orderId', 'customerId', 'date', 'rate', 'advanceAmount', 'submittionDate', 'submittedDate', 'design', 'status', 'remark')

class BillDisplay(admin.ModelAdmin):
    list_display= ('billId', 'customerId', 'orderId', 'date', 'rate', 'customerProductWeight', 'customerProductAmount', 'totalAmount', 'discount', 'grandTotalAmount', 'advanceAmount', 'payedAmount', 'remainingAmount', 'status')

# Register your models here.
admin.site.register(Customer, CustomerDisplay)
admin.site.register(Order, OrderDisplay)
admin.site.register(Bill, BillDisplay)