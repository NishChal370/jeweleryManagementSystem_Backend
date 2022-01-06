from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Customer(models.Model):
    customerId = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return f'{self.customerId}'


class Order(models.Model):
    orderId = models.AutoField(primary_key=True, null=False)
    customerId = models.ForeignKey(Customer, null=True, on_delete=CASCADE, related_name='orders')
    date = models.DateField(null=False)
    rate = models.IntegerField(null=True)
    advanceAmount = models.IntegerField(null=True)
    submittionDate = models.DateField(null=False)
    submittedDate = models.DateField(null=True)
    design = models.ImageField( null=True, blank=True)
    status = models.TextField(null=True)
    remark = models.TextField(null=True)

    def __str__(self):
        return f'{self.orderId}'


class Bill(models.Model):
    bill_status = [
        ('D','Draft'),
        ('S','Submitted')
    ]

    billId =  models.AutoField(primary_key=True, null=False)
    orderId = models.ForeignKey(Order, null=True, on_delete=CASCADE, related_name='customerOrder')
    customerId = models.ForeignKey(Customer, null=True, on_delete=CASCADE, related_name='customerBill')
    date = models.DateField(null=False)
    rate = models.IntegerField(null=True)
    customerProductWeight = models.IntegerField(null=True)
    customerProductAmount = models.IntegerField(null=True)
    totalAmount = models.IntegerField(null=True)
    discount = models.IntegerField(null=True)
    grandTotalAmount = models.IntegerField(null=True)
    advanceAmount = models.IntegerField(null=True)
    payedAmount = models.IntegerField(null=True)
    remainingAmount = models.IntegerField(null=True)
    status = models.CharField(max_length=11, null=False, choices=bill_status, default='Submitted')

    def __str__(self):
        return f'{self.billId}'