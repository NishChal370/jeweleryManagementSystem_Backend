
from django.db.models import fields
from rest_framework import serializers

from .models import Bill, Customer, Order

class OrderSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__' 

class BillSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'


class CustomerSerilizer(serializers.ModelSerializer):
    orders = OrderSerilizer(required=False, many=True, read_only=False, allow_null=True )
    bills = BillSerilizer(required=False, many=True, read_only=False, allow_null=True)

    class Meta:
        model = Customer
        fields = ('customerId', 'name', 'address', 'phone', 'email', 'bills','orders')
        
    def validate(self, value):
        if 'orders' not in value and 'bills' not in value:
            raise serializers.ValidationError({'data':'Customer must have order or bill.'})
        
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
