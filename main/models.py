from asyncio.windows_events import NULL
import email
from turtle import mode
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

import datetime
from django.utils.timezone import now


from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length=30, null=True, blank=True)
    pan_number = models.FloatField(null=True, blank = True)
    phone = models.FloatField(null=True, blank = True)
    register_date = models.DateField(null=True, blank=True)


# Create your models here.
class Customer(models.Model):
    customerId = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=10, null=True , blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f'{self.customerId}'


class Order(models.Model):
    order_status = [
        ('pending','PENDING'),
        ('inprogress','INPROGRESS'),
        ('completed', 'COMPLETED'),
        ('submitted','SUBMITTED'),
    ]
    order_type = [
        ('gold', 'GOLD'),
        ('silver', 'SILVER')
    ]

    orderId = models.AutoField(primary_key=True, null=False)
    customerId = models.ForeignKey(Customer, null=True, on_delete=CASCADE, related_name='orders')
    date = models.DateField(null=False, default=now)
    rate = models.FloatField(null=True, blank = True)
    advanceAmount = models.FloatField(null=True, blank = True)
    submittionDate = models.DateField(null=False, blank = True)
    submittedDate = models.DateField(null=True, blank = True)
    remark = models.TextField(null=True, blank=True)

    customerProductWeight = models.FloatField(null=True, blank = True)
    type = models.CharField(max_length=11, null=False, choices=order_type, default='gold')
    status = models.CharField(max_length=11, null=False, choices=order_status, default='pending')
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
    customerProductWeight = models.FloatField(null=True, blank=True, default=0)
    customerProductAmount = models.FloatField(null=True, blank=True)
    finalWeight = models.FloatField(null=True, blank=True)
    grandTotalWeight = models.FloatField(null=True, blank=True)
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
    netWeight = models.FloatField(null=True, blank=True)
    size = models.FloatField(null=True, blank=True, default=0)
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
        ('pending','PENDING'),
        ('inprogress','INPROGRESS'),
        ('completed','COMPLETED'),
    ]
    orderProductId = models.AutoField(primary_key=True, null=False)
    orderId = models.ForeignKey(Order, null=True, on_delete=CASCADE, related_name='orderProducts')
    productId = models.ForeignKey(Product, null=True, on_delete=CASCADE, related_name='orderProduct')
    totalWeight = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=11, null=False, choices=order_status, default='pending')

    design = models.ImageField(null=True, blank=True, upload_to='images', )
    quantity = models.FloatField(null=True, blank=True, default=1)
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


class Staff(models.Model):
    staffId = models.AutoField(primary_key=True,null=False)
    staffName = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=10, null=True , blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    registrationDate = models.DateField(null=True, blank=True, default=datetime.date.today())
    resignDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.staffId}'


class StaffWork(models.Model):
    work_status = [
        ('inprogress','INPROGRESS'),
        ('completed','COMPLETED'),
    ]

    staffWorkId = models.AutoField(primary_key=True,null=False)
    staff = models.ForeignKey(Staff, null=False, on_delete=CASCADE, related_name='staffwork')
    orderProduct = models.ForeignKey(OrderProduct, null=False, on_delete=CASCADE, related_name='orderProduct')
    date = models.DateField(null=True, blank=True, default=datetime.date.today())
    givenWeight = models.FloatField(null=False)
    KDMWeight = models.FloatField(null=False)
    totalWeight = models.FloatField(null=False)
    submittionDate = models.DateField(null=True, blank=True)
    submittedWeight = models.FloatField(null=True, blank=True)
    finalProductWeight = models.FloatField(null=True, blank=True)
    lossWeight = models.FloatField(null=True, blank=True)
    submittedDate = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=11, null=False, choices=work_status, default='inprogress')

    def __str__(self):
        return f'{self.staffWorkId}'




import json

with open('mail.json','r') as input_file:
    email_data = json.load(input_file)
    email_address = email_data['EMAIL']
    

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = reset_password_token.key
    # email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    print(reset_password_token.key)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Gitanjali Jewellers"),
        # message:
        email_plaintext_message,
        # from:
        email_address,
        # "gitanjalijewellers00@gmail.com",
        # to:
        [reset_password_token.user.email]
        
    )