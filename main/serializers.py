
from django.db import models
from rest_framework import fields, serializers


from .models import Customer, Order

class OrderSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__' 


class CustomerSerilizer(serializers.ModelSerializer):
    orders = OrderSerilizer(many=True, read_only=False)

    class Meta:
        model = Customer
        fields = ('customerId', 'name', 'address', 'phone', 'email', 'orders')

    def create(self, validated_data):
        #get order from the request body
        orders = validated_data.pop('orders') 
        # save customer
        customer = Customer.objects.create(**validated_data) 
        # save order list 
        for orders in orders:
            Order.objects.create(customerId=customer, **orders)

        return customer

