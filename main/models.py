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
    customerId = models.ForeignKey(Customer, null=False, on_delete=CASCADE)
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