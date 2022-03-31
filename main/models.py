from asyncio.windows_events import NULL
import email
from turtle import mode
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.core.mail import EmailMultiAlternatives

import datetime
from django.utils.timezone import now


from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.contrib.auth.models import AbstractUser

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

def upload_to(instance, filename):
      return 'adminImage/{filename}'.format(filename=filename)

class User(AbstractUser):
    full_name = models.CharField(max_length=30, null=True, blank=True)
    pan_number = models.FloatField(null=True, blank = True)
    phone = models.FloatField(null=True, blank = True)
    profileImage = models.ImageField(upload_to=upload_to, null=True, blank=True)
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
    qr_code = models.ImageField(upload_to='qr_code', blank=True)

    def __str__(self):
        return f'{self.billId}'

    def save(self, *args, **kwargs):
        customer = Customer.objects.get(customerId = self.customerId.customerId)
        last_bill = Bill.objects.all().order_by('-billId')[:1][0]
        data = f'''Invoice no = {str(int(last_bill.billId)+1)} \nName = {customer.name} \nDate = {self.date} \nBill Type = {self.billType} \nTotal Amount = {self.grandTotalAmount} \nAdvance = {self.advanceAmount} \nremainingAmount = {self.remainingAmount}'''
        qrcode_img = qrcode.make(data)
        canvas = Image.new('RGB',(600,600), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr-code-{str(int(last_bill.billId)+1)}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)





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





@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    text_content = 'Password Reset Seems like you forget your password for Gitanjali Jewellers. If this is true,Click below to reset your password. If you don\'t mean to reset your password, then you can just ignore this enail; your password will not change.'
    html_content = '<div style="Color:black;"><h1 style="margin:1rem 0rem 0rem 35%; color:#012970; font-size:3rem;" >Password Reset</h1><br/><div style="margin:0rem 0rem 3rem 17%; font-size:1.2rem;">Seems like you forget your password for Gitanjali Jewellers. If this is true, Click below to reset your password.</div><br/><a href="http://localhost:3000/?token='+reset_password_token.key+'" style="margin:1rem 0rem 1rem 39%; color:white; background-color:green; padding:1rem; border-radius:0.6rem; font-size:1.3rem; text-decoration: none;">Choose a new password</a><br/><div style="margin:3rem 0rem 0rem 28%"> If you don\'t mean to reset your password, then you can just ignore this email; your password will not change.</div></div>'
    msg = EmailMultiAlternatives(
        "Reset Password",
        text_content,
        None,
        [reset_password_token.user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()