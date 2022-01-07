from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.timezone import now

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
    date = models.DateField(null=False, default=now)
    rate = models.IntegerField(null=True, blank = True)
    advanceAmount = models.IntegerField(null=True, blank = True)
    submittionDate = models.DateField(null=False, blank = True)
    submittedDate = models.DateField(null=True, blank = True)
    design = models.ImageField( null=True, blank=True)
    status = models.TextField(null=True)
    remark = models.TextField(null=True)

    def __str__(self):
        return f'{self.orderId}'


class Bill(models.Model):
    bill_status = [
        ('D','Draft'),
        ('S','Submitted'),
    ]

    billId =  models.AutoField(primary_key=True, null=False)
    orderId = models.ForeignKey(Order, null=True, on_delete=CASCADE, related_name='orders')
    customerId = models.ForeignKey(Customer, null=True, on_delete=CASCADE, related_name='bills')
    date = models.DateField(null=False, default=now)
    rate = models.IntegerField(null=True, blank=True)
    customerProductWeight = models.IntegerField(null=True, blank=True)
    customerProductAmount = models.IntegerField(null=True, blank=True)
    totalAmount = models.IntegerField(null=True)
    discount = models.IntegerField(null=True, blank=True)
    grandTotalAmount = models.IntegerField(null=True)
    advanceAmount = models.IntegerField(null=True, blank=True)
    payedAmount = models.IntegerField(null=True, blank=True)
    remainingAmount = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=11, null=False, choices=bill_status, default='Submitted')

    def __str__(self):
        return f'{self.billId}'


