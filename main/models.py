from turtle import mode
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

import datetime
from django.utils.timezone import now



# Create your models here.
class Customer(models.Model):
    customerId = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f'{self.customerId}'


class Order(models.Model):
    orderId = models.AutoField(primary_key=True, null=False)
    customerId = models.ForeignKey(Customer, null=True, on_delete=CASCADE, related_name='orders')
    date = models.DateField(null=False, default=now)
    rate = models.FloatField(null=True, blank = True)
    advanceAmount = models.FloatField(null=True, blank = True)
    submittionDate = models.DateField(null=False, blank = True)
    submittedDate = models.DateField(null=True, blank = True)
    design = models.ImageField( null=True, blank=True)
    status = models.TextField(null=True)
    remark = models.TextField(null=True)

    def __str__(self):
        return f'{self.orderId}'


class Bill(models.Model):
    bill_status = [
        ('draft','DRAFT'),
        ('submitted','SUBMITTED'),
    ]

    bill_type =[
        ('gold', 'GOLD'),
        ('silver', 'SILVER')
    ]

    billId =  models.AutoField(primary_key=True, null=False)
    orderId = models.ForeignKey(Order, null=True, blank=True, on_delete=CASCADE, related_name='orders')
    customerId = models.ForeignKey(Customer, null=True, on_delete=CASCADE, related_name='bills')
    date = models.DateField(null=False, default=now)
    rate = models.FloatField(null=True, blank=True)
    billType = models.CharField(max_length=11, null=False, choices=bill_type, default='gold')
    customerProductWeight = models.FloatField(null=True, blank=True)
    customerProductAmount = models.FloatField(null=True, blank=True)
    finalWeight = models.FloatField(null=True, blank=True)
    grandWeight = models.FloatField(null=True, blank=True)
    totalAmount = models.FloatField(null=True)
    discount = models.FloatField(null=True, blank=True)
    grandTotalAmount = models.FloatField(null=True)
    advanceAmount = models.FloatField(null=True, blank=True)
    payedAmount = models.FloatField(null=True, blank=True)
    remainingAmount = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=11, null=False, choices=bill_status, default='submitted')

    def __str__(self):
        return f'{self.billId}'



class Product(models.Model):
    productId = models.AutoField(primary_key=True, null=False)
    productName = models.CharField(max_length=50, null=False)
    netWeight = models.FloatField()
    size = models.FloatField()
    gemsName = models.CharField(max_length=50, null=True, blank=True)
    gemsPrice = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.productId}'


class BillProduct(models.Model):
    billProductId = models.AutoField(primary_key=True, null=False)
    billId = models.ForeignKey(Bill, null=True, on_delete=CASCADE, related_name='billProduct')
    productId = models.ForeignKey(Product, null=True, blank=True, on_delete=CASCADE, related_name='product')
    lossWeight = models.FloatField(null=True, blank=True)
    totalWeight = models.FloatField(null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True, default=1)
    rate = models.FloatField(null=True, blank=True)
    makingCharge = models.FloatField(null=True, blank=True)
    totalAmountPerProduct = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.billProductId}'


class OrderProduct(models.Model):
    order_status = [
        ('P','Pending'),
        ('S','Submitted'),
    ]
    orderProductId = models.AutoField(primary_key=True, null=False)
    orderId = models.ForeignKey(Order, null=True, on_delete=CASCADE, related_name='orderProducts')
    productId = models.ForeignKey(Product, null=True, on_delete=CASCADE, related_name='orderProduct')
    totalWeight = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=11, null=False, choices=order_status, default='Pending')

    def __str__(self):
        return f'{self.orderProductId}'




class Rate(models.Model):
    rateId = models.AutoField(primary_key=True, null=False)
    date = models.DateField(null=True, blank=True, default=datetime.date.today())
    hallmarkRate = models.FloatField(null=False)
    tajabiRate = models.FloatField(null=False)
    silverRate = models.FloatField(null=False)

    def __str__(self):
        return f'{self.rateId}'