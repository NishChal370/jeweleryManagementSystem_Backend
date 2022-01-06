from django.contrib import admin

from .models import Customer, Order

class CustomerDisplay(admin.ModelAdmin):
    list_display = ('customerId', 'name', 'address', 'phone', 'email')

class OrderDisplay(admin.ModelAdmin):
    list_display = ('orderId', 'customerId', 'date', 'rate', 'advanceAmount', 'submittionDate', 'submittedDate', 'design', 'status', 'remark')

# Register your models here.
admin.site.register(Customer, CustomerDisplay)
admin.site.register(Order, OrderDisplay)