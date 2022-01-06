
from rest_framework import serializers


from .models import Customer, Order

class OrderSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__' 


class CustomerSerilizer(serializers.ModelSerializer):
    orders = OrderSerilizer(required=False, many=True, read_only=False, allow_null=True )

    class Meta:
        model = Customer
        fields = ('customerId', 'name', 'address', 'phone', 'email', 'orders')

    def create(self, validated_data):
        # save customer
        customer = Customer.objects.create(**validated_data) 

        #get order from the request body if exists 
        if('orders' in validated_data):
            orders = validated_data.pop('orders') 
            # save order list 
            for order in orders:
                Order.objects.create(customerId=customer, **order)

        return customer

