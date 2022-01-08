
from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Bill, BillProduct, Customer, Order, Product

##Product
class ProductSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

##BillProduct
class BillProductSerilizer(serializers.ModelSerializer):
    product = ProductSerilizer(required=False, many=False, read_only=False, allow_null=True )
    class Meta:
        model = BillProduct
        #fields = ('billId', 'lossWeight', 'totalWeight', 'rate', 'makingCharge', 'totalAmountPerProduct','products')
        fields = '__all__'

##Order
class OrderSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__' 

##Bill
class BillSerilizer(serializers.ModelSerializer):
    billProduct = BillProductSerilizer(required=False, many=True, read_only=False, allow_null=True )
    class Meta:
        model = Bill
        fields = ('billId', 'orderId', 'customerId', 'date', 'rate', 'customerProductWeight', 'customerProductAmount', 'totalAmount', 'discount', 'grandTotalAmount', 'advanceAmount', 'payedAmount', 'remainingAmount', 'status', 'billProduct')


"""
 # it register customer and add their generate their bill.
 # if customer already register  generate bill for existing customer
"""
class GenerateBillSerilizer(serializers.ModelSerializer):
    bills = BillSerilizer(required=False, many=True, read_only=False, allow_null=True)
    class Meta:
        model = Customer
        fields = ('customerId', 'name', 'address', 'phone', 'email', 'bills')

    def validate(self, value):
        if 'bills' not in value :
            raise serializers.ValidationError({'message':'Bill is missing.'})
        elif len(value['bills']) < 1:
            raise serializers.ValidationError({'message':'Bill is missing.'})

        for bill in value['bills']:
            if 'billProduct' not in bill:
                raise serializers.ValidationError({'message':'BillProduct is missing.'})
            elif len(bill['billProduct']) < 1:
                raise serializers.ValidationError({'messsage':'BillProduct is missing.'}) 

            for billProduct in bill['billProduct']:
                if 'product' not in billProduct:
                    raise serializers.ValidationError({'message':'Product is missing.'})

        return value


    def create(self, validated_data):
        bills = validated_data.pop('bills')
        #create customer
        customer = Customer.objects.create(**validated_data) 

        for bill in bills :
            billProducts = bill.pop('billProduct')
            #create bill
            newBill = Bill.objects.create(customerId=customer, **bill)

            for billProduct in billProducts:
                product = billProduct.pop('product')
                #create product
                newProduct = Product.objects.create(**product)
                #create billProduct
                BillProduct.objects.create(billId=newBill, productId=newProduct, **billProduct)
                
        return customer
    
    def update(self, instance, validated_data):
        bills = validated_data.pop('bills')

        for bill in bills :
            billProducts = bill.pop('billProduct')
            #add bill in for existing customer
            newBill = Bill.objects.create(customerId=instance, **bill)

            for billProduct in billProducts:
                product = billProduct.pop('product')
                # add product for existing customer
                newProduct = Product.objects.create(**product)
                # add billProduct for existing customer
                BillProduct.objects.create(billId=newBill, productId=newProduct, **billProduct)

        return instance


'''
 #Register customer with order or bill 
 #if customer exist add bill or order in existing customer
'''
class CustomerSerilizer(serializers.ModelSerializer):
    orders = OrderSerilizer(required=False, many=True, read_only=False, allow_null=True )
    bills = BillSerilizer(required=False, many=True, read_only=False, allow_null=True)

    class Meta:
        model = Customer
        fields = ('customerId', 'name', 'address', 'phone', 'email', 'bills','orders')
        
    def validate(self, value):
        if 'orders' not in value and 'bills' not in value:
            raise serializers.ValidationError({'message':'Customer must have order or bill.'})
        
        return value

    def create(self, validated_data):  
        #get bill from the request body 
        bills  = validated_data.pop('bills')
        #get order from the request body
        orders = validated_data.pop('orders') if 'orders' in validated_data else []
        
        # save customer
        customer = Customer.objects.create(**validated_data) 

        # save order list 
        for order in orders:
            Order.objects.create(customerId=customer, **order)

        # save bill list
        for bill in bills:
            Bill.objects.create(customerId = customer, **bill)

        return customer
    
    def update(self, instance, validated_data):
        if('bills' in validated_data):
            #get bill from the request body 
            bills  = validated_data.pop('bills')

            # many bills
            for bill in bills:
                Bill.objects.create(customerId = instance, **bill)

        if('orders' in validated_data):
            #get order from the request body
            orders = validated_data.pop('orders')

            # save order list 
            for order in orders:
                Order.objects.create(customerId=instance, **order)

        return instance
