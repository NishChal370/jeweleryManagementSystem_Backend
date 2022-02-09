import re
from django.db import models
from django.db.models import fields
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Bill, BillProduct, Customer, Order, OrderProduct, Product, Rate


'''
 # Product
'''
class ProductSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('productId', 'productName', 'netWeight', 'size', 'gemsName', 'gemsPrice')



'''
 # BillProduct
'''
class BillProductSerilizer(serializers.ModelSerializer):
    product = ProductSerilizer(required=False, many=False, read_only=False, allow_null=True )
    class Meta:
        model = BillProduct
        # remove billProductId if some error
        fields = ('billProductId', 'billId', 'quantity', 'lossWeight', 'totalWeight', 'rate', 'makingCharge', 'totalAmountPerProduct','product')
    
    def to_representation(self, instance): # it shows all the product insted of id
        rep = super().to_representation(instance)
        rep['product'] = ProductSerilizer(instance.productId).data
        return rep



'''
 # OrderProduct
'''
class OrderProductSerilizer(serializers.ModelSerializer):
    # orderProduct = ProductSerilizer(required=False, many=False, read_only=False, allow_null=True )
    product = ProductSerilizer(required=False, many=False, read_only=False, allow_null=True )
    class Meta:
        model = OrderProduct
        # fields = ('orderProductId', 'orderId', 'productId', 'totalWeight', 'status', 'orderProduct')
        fields = ('orderProductId', 'orderId', 'totalWeight', 'status', 'product')
    def to_representation(self, instance): # it shows all the product insted of id
        rep = super().to_representation(instance)
        rep['product'] = ProductSerilizer(instance.productId).data
        return rep


'''
 # Order
'''
class OrderSerilizer(serializers.ModelSerializer):
    orderProducts = OrderProductSerilizer(required=False, many=True, read_only=False, allow_null=True )
    class Meta:
        model = Order
        # fields = ('orderId', 'customerId', 'date', 'rate', 'advanceAmount', 'submittionDate', 'submittedDate', 'design', 'status', 'remark', 'orderProducts')
        fields = ('orderId', 'customerId', 'date', 'billType', 'rate', 'customerProductWeight', 'advanceAmount', 'submittionDate', 'submittedDate', 'status', 'remark' ,'orderProducts')



'''
 # Bill
'''
class BillSerilizer(serializers.ModelSerializer):
    billProduct = BillProductSerilizer(required=False, many=True, read_only=False, allow_null=True )
    class Meta:
        model = Bill
        fields = ('billId', 'orderId', 'customerId', 'date', 'rate', 'billType', 'customerProductWeight', 'customerProductAmount', 'finalWeight', 'grandTotalWeight', 'totalAmount', 'discount', 'grandTotalAmount', 'advanceAmount', 'payedAmount', 'remainingAmount', 'status', 'billProduct')



'''
    # to get all bill  and its customers in detail
'''
class BillDetailSerilizer(serializers.ModelSerializer):
    billProduct = BillProductSerilizer(required=False, many=True, read_only=False, allow_null=True )

    class Meta:
        model = Bill
        fields = ('billId', 'orderId','date', 'rate', 'billType', 'customerProductWeight', 'customerProductAmount', 'finalWeight', 'grandTotalWeight', 'totalAmount', 'discount', 'grandTotalAmount', 'advanceAmount', 'payedAmount', 'remainingAmount', 'status', 'billProduct')
    
    def to_representation(self, instance): # it shows all the customer insted of id
        rep = super().to_representation(instance)
        rep['customer'] = CustomerInfoSerilizer(instance.customerId).data

        return rep



'''
# search bill in summary
'''
class BillSearchSerilizer(serializers.ModelSerializer, APIView):
    billProduct = BillProductSerilizer(required=False, many=True, read_only=False, allow_null=True )

    class Meta:
        model = Bill
        fields = ('billId', 'orderId', 'customerId', 'date', 'rate', 'billType', 'customerProductWeight', 'customerProductAmount', 'finalWeight', 'grandTotalWeight', 'totalAmount', 'discount', 'grandTotalAmount', 'advanceAmount', 'payedAmount', 'remainingAmount', 'status', 'billProduct')

    def to_representation(self, data):
        searchData = {'billId': '', 'customerId':'', 'customerName':'',  'phone':'', 'type':'', 'totalProduct': '', 'productsWeight':'', 'customerProductWeight': '', 'status':  '', 'payment': '', 'date': ''}
        
        rep = super().to_representation(data)
        customer = CustomerSerilizer(data.customerId).data

        if(rep['remainingAmount']  == None):
            rep['remainingAmount'] = 0

        if(rep['remainingAmount'] > 0 ):
            searchData['payment'] = "Remain"
        else:
           searchData['payment'] = "Payed"
        
        searchData['date'] = rep['date']
        searchData['billId'] = rep['billId']
        searchData['type'] = rep['billType']
        searchData['status'] = rep['status']
        searchData['phone'] = customer['phone']
        searchData['customerId'] = customer['customerId']
        searchData['customerName'] = customer['name']
        searchData['customerAddress'] = customer['address']
        searchData['productsWeight'] = rep['finalWeight']
        searchData['totalProduct'] = len(rep['billProduct'])
        searchData['customerProductWeight'] = rep['customerProductWeight']

        return searchData



'''
 # Rate
'''
class RateSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('rateId', 'date', 'hallmarkRate', 'tajabiRate', 'silverRate')



"""
 # it register customer and add / generate their bill.
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
 # Product
'''
class ProductForUpdateSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('productId', 'productName', 'netWeight', 'size', 'gemsName', 'gemsPrice')
        extra_kwargs = {'productId': {'required':False,'read_only':False, 'allow_null':True}}

'''
 # BillProduct
'''
class BillProductForUpdateSerilizer(serializers.ModelSerializer):
    product = ProductForUpdateSerilizer(required=False, many=False, read_only=False, allow_null=True )
    class Meta:
        model = BillProduct
        # remove billProductId if some error
        fields = ('billProductId', 'billId', 'quantity', 'lossWeight', 'totalWeight', 'rate', 'makingCharge', 'totalAmountPerProduct','product')
        extra_kwargs = {'billProductId': {'required':False,'read_only':False, 'allow_null':True}}
    
    def to_representation(self, instance): # it shows all the product insted of id
        rep = super().to_representation(instance)
        rep['product'] = ProductSerilizer(instance.productId).data
        return rep

'''
 # Bill
'''
class BillForUpdateSerilizer(serializers.ModelSerializer):
    billProduct = BillProductForUpdateSerilizer(required=False, many=True, read_only=False, allow_null=True )
    class Meta:
        model = Bill
        fields = ('billId', 'orderId', 'customerId', 'date', 'rate', 'billType', 'customerProductWeight', 'customerProductAmount', 'finalWeight', 'grandTotalWeight', 'totalAmount', 'discount', 'grandTotalAmount', 'advanceAmount', 'payedAmount', 'remainingAmount', 'status', 'billProduct')
        extra_kwargs = {'billId': {'required':False,'read_only':False, 'allow_null':True}}



'''
 # Update saved bill {edit, delete}
'''
class UpdateExistingBillSerilizer(serializers.ModelSerializer):
    bills = BillForUpdateSerilizer(required=False, many=True, read_only=False, allow_null=True)

    class Meta:
        model = Customer
        fields = ('customerId', 'name', 'address', 'phone', 'email', 'bills')
        
    def update(self, instance, validated_data):
        bill = validated_data.pop('bills')[0]

        Customer.objects.filter(customerId = instance.customerId).update(**validated_data)

        billProducts = bill.pop('billProduct')

        Bill.objects.filter(billId= bill.get('billId')).update(**bill)

        keep_ProductId_list = []
        for billProduct in billProducts:
            product = billProduct.pop('product')
            #if new billProduct 
            if 'billProductId' not in billProduct.keys():
                newProduct = Product.objects.create(**product)

                bill = Bill.objects.get(billId = bill.get('billId'))
                BillProduct.objects.create(billId=bill, productId=newProduct, **billProduct)

                keep_ProductId_list.append(newProduct.productId)
            #if billProduct exists
            else:
                Product.objects.filter(productId = product.get('productId')).update(**product)
                BillProduct.objects.filter(billProductId= billProduct.get('billProductId')).update(**billProduct)

                keep_ProductId_list.append(product.get('productId'))

        existing_ProductId_list = [c.productId for c in BillProduct.objects.filter(billId = bill.get('billId'))]  
        #if product to be deleted
        for existing_ProductId in existing_ProductId_list:
            if existing_ProductId.productId not in keep_ProductId_list:
                product = Product.objects.get(productId = existing_ProductId.productId)
                product.delete()

        return Customer.objects.get(customerId=instance.customerId)



"""
 # it register customer and add / generate their Order.
 # if customer already register  generate Order for existing customer
"""
class PlaceOrderSerilizer(serializers.ModelSerializer):
    orders = OrderSerilizer(required=False, many=True, read_only=False, allow_null=True)
    class Meta:
        model = Customer
        fields = ('customerId', 'name', 'address', 'phone', 'email', 'orders')

    def validate(self, value):
        if 'orders' not in value :
            raise serializers.ValidationError({'message':'Order is missing.'})
        elif len(value['orders']) < 1:
            raise serializers.ValidationError({'message':'Order is missing.'})

        for order in value['orders']:
            if 'orderProducts' not in order:
                raise serializers.ValidationError({'message':'OrderProduct is missing.'})
            elif len(order['orderProducts']) < 1:
                raise serializers.ValidationError({'messsage':'OrderProduct is missing.'}) 

            for orderProducts in order['orderProducts']:
                # if 'orderProduct' not in orderProducts:
                if 'product' not in orderProducts:
                    raise serializers.ValidationError({'message':'Product is sssmissing.'})

        return value


    def create(self, validated_data):
        orders = validated_data.pop('orders')
        #create customer
        customer = Customer.objects.create(**validated_data) 

        for order in orders :
            orderProducts = order.pop('orderProducts')
            #create order
            newOrder = Order.objects.create(customerId=customer, **order)

            for orderProduct in orderProducts:
                # product = orderProduct.pop('orderProduct')
                product = orderProduct.pop('product')
                #create product
                newProduct = Product.objects.create(**product)
                #create orderProduct
                OrderProduct.objects.create(orderId=newOrder, productId=newProduct, **orderProduct)
                
        return customer
    
    def update(self, instance, validated_data):
        orders = validated_data.pop('orders')

        for order in orders :
            orderProducts = order.pop('orderProducts')
            #add Order in for existing customer
            newOrder = Order.objects.create(customerId=instance, **order)

            for orderProduct in orderProducts:
                # product = orderProduct.pop('orderProduct')
                product = orderProduct.pop('product')
                # add product for existing customer
                newProduct = Product.objects.create(**product)
                # add orderProduct for existing customer
                OrderProduct.objects.create(orderId=newOrder, productId=newProduct, **orderProduct)

        return instance



'''
Create bill for order
'''
class OrderBillSerilizer(serializers.ModelSerializer):
    billProduct = BillProductSerilizer(required=False, many=True, read_only=False, allow_null=True )
    class Meta:
        model= Bill
        fields= ('billId', 'orderId', 'customerId', 'date', 'rate', 'customerProductWeight', 'customerProductAmount', 'totalAmount', 'discount', 'grandTotalAmount', 'advanceAmount', 'payedAmount', 'remainingAmount', 'status', 'billProduct')
    
    def validate(self, value):
        if 'orderId' not in value:
            
            raise serializers.ValidationError({'message':'orderId is missing'})
        #elif value['orderId'].status == 'S': // UNCOMMMENT LATER 

            #raise serializers.ValidationError({'message':'Requested order bill is already created'}) // UNCOMMMENT LATER 
        
        return value

    def create(self, validated_data):
        order= validated_data['orderId']
        #get customerId from order and set to bills customerId
        validated_data['customerId'] = order.customerId
        orderProduct = OrderProduct.objects.get(orderId = order.orderId)

        bill = Bill.objects.create(**validated_data) 
        BillProduct.objects.create(billId=bill, productId=orderProduct.productId, totalWeight= orderProduct.totalWeight)

        order.status = 'S'
        order.save()
        OrderSerilizer(order)

        return bill



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



'''
    # Get customer Detail only
'''
class CustomerInfoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customerId', 'name', 'address', 'phone', 'email')



'''
    # Get bill Detail only
'''
class BillInfoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ('billId', 'orderId', 'customerId', 'date', 'rate', 'billType', 'customerProductWeight', 'customerProductAmount', 'finalWeight', 'grandTotalWeight', 'totalAmount', 'discount', 'grandTotalAmount', 'advanceAmount', 'payedAmount', 'remainingAmount', 'status')



'''
 # BillProduct detail only
'''
class BillProductInfoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = BillProduct
        fields = ('billProductId', 'billId', 'productId', 'quantity', 'lossWeight', 'totalWeight', 'rate', 'makingCharge', 'totalAmountPerProduct')



# class UpdateExistingBillSerilizer(serializers.ModelSerializer):
#     # billProduct = BillProductSerilizer(required=False, many=True, read_only=False, allow_null=True )
#     class Meta:
#         model = Bill
#         fields = ('billId', 'orderId', 'customer', 'date', 'rate', 'billType', 'customerProductWeight', 'customerProductAmount', 'finalWeight', 'grandTotalWeight', 'totalAmount', 'discount', 'grandTotalAmount', 'advanceAmount', 'payedAmount', 'remainingAmount', 'status')

#         # fields = ('billId', 'orderId','date', 'rate', 'billType', 'customerProductWeight', 'customerProductAmount', 'finalWeight', 'grandTotalWeight', 'totalAmount', 'discount', 'grandTotalAmount', 'advanceAmount', 'payedAmount', 'remainingAmount', 'status', 'billProduct','customerId')
    
#     # def to_representation(self, instance): # it shows all the customer insted of id
#     #     rep = super().to_representation(instance)
#     #     rep['customer'] = CustomerInfoSerilizer(instance.customer.customerId).data

#     #     return rep

#     def update(self, instance, validate_data):
#         print("FDgdfgdfgdfgdfg")
#         print("Update")
#         print(instance)
#         print()
#         # validate_data['customer'] = instance['customer']
#         print(validate_data)
#         return instance



























# # """
# #  # it register customer and add / generate their bill.
# #  # if customer already register  generate bill for existing customer
# # """
# # class GenerateBillSerilizer(serializers.ModelSerializer):
# #     bills = BillSerilizer(required=False, many=True, read_only=False, allow_null=True)
# #     class Meta:
# #         model = Customer
# #         fields = ('customerId', 'name', 'address', 'phone', 'email', 'bills')

# #     def validate(self, value):
# #         print(value)
# #         if 'bills' not in value :
# #             raise serializers.ValidationError({'message':'Bill is missing.'})
# #         elif len(value['bills']) < 1:
# #             raise serializers.ValidationError({'message':'Bill is missing.'})

# #         for bill in value['bills']:
# #             if 'billProduct' not in bill:
# #                 raise serializers.ValidationError({'message':'BillProduct is missing.'})
# #             elif len(bill['billProduct']) < 1:
# #                 raise serializers.ValidationError({'messsage':'BillProduct is missing.'}) 

# #             for billProduct in bill['billProduct']:
                
# #                 if 'product' not in billProduct:
# #                     raise serializers.ValidationError({'message':'Product is missing.'})

# #         return value


# #     def create(self, validated_data):
# #         bills = validated_data.pop('bills')
# #         #create customer
# #         customer = Customer.objects.create(**validated_data) 

# #         for bill in bills :
# #             billProducts = bill.pop('billProduct')
# #             #create bill
# #             newBill = Bill.objects.create(customerId=customer, **bill)

# #             for billProduct in billProducts:
# #                 product = billProduct.pop('product')
# #                 #create product
# #                 newProduct = Product.objects.create(**product)
# #                 #create billProduct
# #                 BillProduct.objects.create(billId=newBill, productId=newProduct, **billProduct)
                
# #         return customer
    
# #     def update(self, instance, validated_data):
# #         bills = validated_data.pop('bills')

# #         for bill in bills :
# #             billProducts = bill.pop('billProduct')
# #             #add bill in for existing customer
# #             newBill = Bill.objects.create(customerId=instance, **bill)

# #             for billProduct in billProducts:
# #                 product = billProduct.pop('product')
# #                 # add product for existing customer
# #                 newProduct = Product.objects.create(**product)
# #                 # add billProduct for existing customer
# #                 BillProduct.objects.create(billId=newBill, productId=newProduct, **billProduct)

# #         return instance
