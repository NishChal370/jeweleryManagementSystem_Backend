
from itertools import product
from math import e
from sqlite3 import Date
import datetime
from traceback import print_tb
from django.utils.timezone import now
from webbrowser import get
from threading import main_thread
#Q objects that allow to complex lookups.
from django.db.models import Q
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from main.models import BillProduct, Customer, Order, Bill, Product, Rate
from main.serializers import BillDetailSerilizer, BillInfoSerilizer, BillProductInfoSerilizer, BillSearchSerilizer, BillSerilizer, CustomerInfoSerilizer, CustomerSerilizer, GenerateBillSerilizer, OrderBillSerilizer, OrderSearchSerilizer, OrderSerilizer, PlaceOrderSerilizer, ProductSerilizer, RateSerilizer, UpdateExistingBillSerilizer



##Create your views here.
def index(response):
    return HttpResponse("Hello from API")


'''
    # Customer
'''
##Get customer with their orders and bills
@api_view(['GET'])
def customerList(request):
    customer = Customer.objects.all()
    serializer = CustomerSerilizer(customer, many = True)

    return Response(serializer.data)



##Get customer by ID
@api_view(['GET'])
def customerById(request, pk):
    try:
        customer = Customer.objects.get(customerId=pk)
        serializer = CustomerInfoSerilizer(customer, many=False)

        return Response(serializer.data)
    except:
        return Response({"message" : "Not Found !!"}, status=status.HTTP_404_NOT_FOUND)



##Register customer with order or bill (or if customer exist add bill or order in existing customer)
@api_view(['POST'])
def placeCustomerOrderOrBill(request):
     
    if(Customer.objects.filter(name= request.data['name']).exists()):
        oldCustomer = Customer.objects.get(name= request.data['name'])
        newCustomerOrder = CustomerSerilizer(instance= oldCustomer, data= request.data)
    else:
        newCustomerOrder = CustomerSerilizer(data= request.data)
        
    if newCustomerOrder.is_valid():
        newCustomerOrder.save()  

        return Response(newCustomerOrder.data)
    else:
        return Response(newCustomerOrder.errors, status=status.HTTP_400_BAD_REQUEST)



'''
    # Order
'''

##Get all order only
@api_view(['GET'])
def orderList(request):
    orders = Order.objects.all()
    serializer = OrderSerilizer(orders, many = True)

    return Response(serializer.data)



##Get order by ID
@api_view(['GET'])
def order(request, pk):
    try:
        order = Order.objects.get(orderId=pk)
        serializer = OrderSerilizer(order, many=False)

        return Response(serializer.data)
    except:
        return Response({"message" : "Not Found !!"}, status=status.HTTP_404_NOT_FOUND)



##Post orders
# # @api_view(['POST'])
# # def placeOrder(request):
# #     newOrder = OrderSerilizer(data= request.data)

# #     if newOrder.is_valid():
# #         newOrder.save()

# #         return Response(newOrder.data)
# #     else:
# #         return Response(newOrder.errors, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework.parsers import MultiPartParser
# from rest_framework.decorators import parser_classes
# @parser_classes((MultiPartParser, ))
##Generate Order
@api_view(['POST'])
def generateOrder(request):
    print(request.data)
    if(Customer.objects.filter(name= request.data['name']).exists()):
        oldCustomer = Customer.objects.get(name= request.data['name'])
        newOrder = PlaceOrderSerilizer(instance= oldCustomer, data= request.data)
    else:
        newOrder = PlaceOrderSerilizer(data= request.data)

    if newOrder.is_valid():
        newOrder.save()

        return Response(newOrder.data)
    else:
        print(newOrder.error_messages)
        print(newOrder._errors)
        print(newOrder.errors)
        return Response(newOrder.errors, status=status.HTTP_400_BAD_REQUEST)



##Getcustomer Order
@api_view(['GET'])
def getOrders(request):
    #get only those customer who have ordered
    customers = Customer.objects.filter(customerId__in = list(Order.objects.values_list('customerId', flat=True)))
    serializer = PlaceOrderSerilizer(customers, many=True)

    return Response(serializer.data)



## GenerateOrderBill
@api_view(['POST'])
def generateOrderBill(request):
    orderBill =  OrderBillSerilizer(data= request.data)
    if orderBill.is_valid():
        orderBill.save()

        return Response(orderBill.data)
    else:

        return Response(orderBill.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def orderListSummary(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    orders =Order.objects.all().order_by('-date', '-orderId')
    result_page = paginator.paginate_queryset(orders, request)

    serializer = OrderSearchSerilizer(result_page, many =True)

    data = paginator.get_paginated_response(serializer.data) # current page with total page
    data.data['pageIndex'] = str(paginator.page).replace('<Page ', '').replace('>', '')

    return data
    # return Response(serilizer.data)



'''
    # Bills
'''

##Get all bills
@api_view(['GET'])
def billsList(request): 
    bills = Bill.objects.all()
    serializer = BillSerilizer(bills, many=True)

    return Response(serializer.data)


##Get bill summary / bill search in frontend
@api_view(['GET'])
def billsListSummmary(request):
    billType = request.GET.get('billType') # Query param
    billStatus = request.GET.get('billStatus')
    billDate = request.GET.get('billDate')
    nowDate = datetime.datetime.now().date()

    paginator = PageNumberPagination()
    paginator.page_size = 21
    
    if(billDate is not None):
        bills = Bill.objects.filter(date__range = [billDate, nowDate]).order_by('-date', '-billId')
    else:
        bills =Bill.objects.all().order_by('-date', '-billId')

    if(billType != 'all'): # fiter by bill type {gold, silver}
        # bills = Bill.objects.filter(billType = billType)
        bills = bills.filter(billType = billType).order_by('-date', '-billId')
    # else:
    #     bills = bills
        # bills = Bill.objects.all()

    if(billStatus != 'all'): # fiter by bill status {submitted, draft}
        bills = bills.filter(status = billStatus).order_by('-date', '-billId')

    if(billDate is None):
        bills = bills.order_by('-date', '-billId')

    result_page = paginator.paginate_queryset(bills, request)

    serializer = BillSearchSerilizer(result_page, many=True)

    data = paginator.get_paginated_response(serializer.data) # current page with total page
    data.data['pageIndex'] = str(paginator.page).replace('<Page ', '').replace('>', '')

    return data



# we can search bill by name, address, phone
@api_view(['GET'])
def getBillSummaryByCustomerInfo(request, searchValue):
    billType = request.GET.get('billType') # Query param
    billStatus = request.GET.get('billStatus')
    billDate = request.GET.get('billDate')
    nowDate = datetime.datetime.now().date()

    paginator = PageNumberPagination()
    paginator.page_size = 21
    searchCustomer = Customer.objects.filter(Q(name__icontains=searchValue) | Q(address__icontains=searchValue) | Q(phone__icontains=searchValue)) # __icontains  it make case insentive

    billsIdList = []
    # getting search customer bills id
    for c in searchCustomer:
        #filter by customnerId
        if(billType == 'all'):
            searchedBills = list(Bill.objects.filter(customerId=c).values_list('billId', flat=True))
        #filter by billType {gold, silver} & customnerId
        else:
            searchedBills = Bill.objects.filter(customerId=c).filter(billType= billType).values_list('billId', flat=True)

        billsIdList.extend(searchedBills)  

    searchedBills = Bill.objects.filter(billId__in=billsIdList)

    if(billDate is not None):
        searchedBills = searchedBills.filter(date__range = [billDate, nowDate])
    else:
        searchedBills =searchedBills.all()

    if(billStatus != 'all'): 
        #fiter by bill status {submitted, draft}
        searchedBills = searchedBills.filter(status = billStatus)
    else:
        searchedBills = searchedBills.order_by('-date', '-billId')

    result_page = paginator.paginate_queryset(searchedBills, request)

    serializer = BillSearchSerilizer(result_page, many=True)
    
    #current page with total page
    data = paginator.get_paginated_response(serializer.data)
    data.data['pageIndex'] = str(paginator.page).replace('<Page ', '').replace('>', '')

    return data    



##Get bill by ID
@api_view(['GET'])
def billById(request, pk):
    try:
        bill = Bill.objects.get(billId=pk)
        serializer = BillDetailSerilizer(bill, many=False)

        return Response(serializer.data)
    except:
        return Response({"message" : "Not Found !!"}, status=status.HTTP_404_NOT_FOUND)


#delete bill by id
@api_view(['DELETE'])
def deleteBillById(request, pk):
    try:
        bill = Bill.objects.get(billId=pk)
        bill.delete()

        bill = Bill.objects.all()

        bill = BillSearchSerilizer(bill, many=True)

        return Response(bill.data)
    except:
        return Response({"message" : "Not Found !!"}, status=status.HTTP_404_NOT_FOUND)

##Get all products
@api_view(['GET'])
def productList(request):
    products = Product.objects.all()
    serializer = ProductSerilizer(products, many=True)

    return Response(serializer.data)



##Generate Bill
@api_view(['POST'])
def generateBill(request):

    if(Customer.objects.filter(name= request.data['name']).exists()):
        oldCustomer = Customer.objects.get(name= request.data['name'])

        newBill = GenerateBillSerilizer(instance= oldCustomer, data= request.data)
    else:
        newBill = GenerateBillSerilizer(data= request.data)

    if newBill.is_valid():
        newBill.save()

        return Response(newBill.data)
    else:
        return Response(newBill.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST']) 
def billUpdate(request):
    oldCustomer = Customer.objects.get(customerId = request.data['customerId'])
    serilizer = UpdateExistingBillSerilizer(instance=oldCustomer, data=request.data)

    if serilizer.is_valid():
        serilizer.save()

        return Response(serilizer.data)
    
    return Response(serilizer.errors)
    


##Get customer bill
@api_view(['GET'])
def getBills(request):
    customers = Customer.objects.all()
    serializer = GenerateBillSerilizer(customers, many=True)

    return Response(serializer.data)



'''
    # Rates
'''

## get all rates
@api_view(['GET'])
def getAllRates(request):
    rates = Rate.objects.all()
    serializer = RateSerilizer(rates, many=True)
    if(len(serializer.data) <=0):
        return Response("Rate data is empty", status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.data)



## set rate
@api_view(['POST'])
def setRate(request):
    existingRate = Rate.objects.filter(date= datetime.datetime.now())
    if(existingRate.exists()):
        oldRate = Rate.objects.get(date= datetime.datetime.now())
        newRate = RateSerilizer(instance= oldRate, data= request.data)
    else:
        newRate = RateSerilizer(data= request.data)

    if newRate.is_valid():
        newRate.save()

        return Response(newRate.data)
    else:

        return Response(newRate.errors, status=status.HTTP_400_BAD_REQUEST)



## Get rate by date
@api_view(['GET'])
def getRateByDate(request, date):
    try:
        rate = Rate.objects.get(date = date)
        serializer = RateSerilizer(rate, many=False)

        return Response(serializer.data)
    except :

       return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)



## update todays rate
@api_view(['POST'])
def updateTodaysRate(request, pk):
    try:
        rate = Rate.objects.get(rateId = pk)
        # allow to update todays date only
        if(rate.date == datetime.date.today()) : 
            updatedRate = RateSerilizer(instance=rate, data=request.data)

            if updatedRate.is_valid():
                updatedRate.save()

                return Response(updatedRate.data)
            else:

                return Response(updatedRate.errors, status=status.HTTP_400_BAD_REQUEST)
        else:

            return Response({"messagee": "Data cannot be updated!!!"}, status=status.HTTP_400_BAD_REQUEST)
    except:

        return Response({"message": "ID "+str(pk)+" Not Found!!"}, status=status.HTTP_400_BAD_REQUEST)




'''
#######class base pagination
from rest_framework.pagination import PageNumberPagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 2

from rest_framework import generics
class billsList(generics.ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerilizer
    pagination_class = StandardResultsSetPagination'''

'''
####function base pagination
from rest_framework.pagination import PageNumberPagination

#Get all bills
@api_view(['GET'])
def billsList(request): 
    paginator = PageNumberPagination()
    paginator.page_size = 1
    bills = Bill.objects.all()
    result_page = paginator.paginate_queryset(bills, request)
    serializer = BillSerilizer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)
'''




##-------------------------------------->>>>>
# @api_view(['POST']) 
# def billUpdate(request):
#     customer = request.data
#     bill = customer.pop('bills')[0]
#     updatingBillId = bill['billId']
#     updatedCustomer = Customer.objects.filter(customerId= customer['customerId']).update(**customer)

#     billProductList = bill.pop('billProduct')
#     updatedBill = Bill.objects.filter(billId= bill['billId']).update(**bill)
#     print(updatedBill)
#     # # bill = Bill.objects.get(billId=updatedBill)
#     bill = Bill.objects.filter(billId=updatingBillId).first()
#     print("Ccccc")
#     print(updatedBill)
#     print(bill)
#     print("Ccccc")
#     lis = []
#     for billProduct in billProductList:
#         print("In")
#         product = billProduct.pop('product')
    
#         if "billProductId" not in  billProduct:
#             # add product for existing customer
#             newProduct = Product.objects.create(**product)

#             # add billProduct for existing customer
            
#             # BillProduct.objects.create(billId=bill, productId=newProduct, **billProduct)
#             newBillProduct = BillProduct.objects.create(billId=bill, productId=newProduct, **billProduct)
#         else:
#             #old product
#             newProduct = Product.objects.filter(productId = product['productId']).update(**product)
#             newBillProduct =BillProduct.objects.filter(billProductId = billProduct['billProductId']).update(**billProduct)
#             print(newBillProduct)
#         print(updatedBill)
#         print(updatingBillId)
#         a = BillProduct.objects.filter(billId = updatingBillId).values_list('billProductId', flat=True)

#         print(a)
#         print(list(a).__contains__(2))
#         print("CHEKC")
#         for b in list(a):
#             print(list(a))
#             print(billProduct)
#         print("DONE")

   
#     #assemblingupdated data in reqd format
#     updatedBill = BillDetailSerilizer(bill, many=False).data
#     updatedCustomer = updatedBill.pop('customer')
#     updatedCustomer['bills'] = updatedBill

#     return Response(updatedCustomer)
##--------------------------------------<<<

# @api_view(['POST']) 
# def billUpdate(request):
#     oldCustomer = Customer.objects.get(customerId = request.data['customerId'])
#     updatedBill = UpdateExistingBillSerilizer(instance=request.data['customerId'], data = request.data)
#     if updatedBill.is_valid():
#         updatedBill.save()
    
#     return Response({"Hello"})

# @api_view(['POST']) 
# def billUpdate(request):

#     print(request.data)
#     print()
    
#     bill =request.data.pop('bills')[0]
#     print("CUSTOMER")
#     print(request.data)
#     print()
#     print("BILL")
#     print(bill)
#     print()
    
#     billProducts = bill.pop('billProduct')
#     print(billProducts)
#     for billProduct in billProducts:
#         print("BILLPRODUCT")
#         print(billProduct)
#         print()
#         product = billProduct.pop('product')
#         print(product)
#     return Response(request.data)



# ##Update bill
# @api_view(['POST']) 
# def billUpdate(request):
#     data = request.data
#     bill = data.pop('bills')[0]
#     #update customer
#     oldCustomer = Customer.objects.get(customerId= data['customerId'])
  
#     updatedCustomer = CustomerInfoSerilizer(instance = oldCustomer, data = data)
#     if updatedCustomer.is_valid():
#         updatedCustomer.save()
#     else:
#         return Response(updatedCustomer.error_messages)
    
#     billProductList = bill.pop('billProduct')
#     #update bill
#     oldBill = Bill.objects.get(billId = bill['billId'])
   
#     updatedBill = BillInfoSerilizer(instance = oldBill, data = bill)
#     if updatedBill.is_valid():
#         updatedBill.save()
#     else:
#         return Response(updatedBill.error_messages)

#     print('5')
#     for billProduct in billProductList:
#         product = billProduct.pop('product')
#         print(product)
#         print(billProduct)
#         # #update Bill product
#         # oldBillProduct = BillProduct.objects.get(billProductId = billProduct['billProductId'])
       
#         # updatedBillProduct = BillProductInfoSerilizer(instance = oldBillProduct, data = billProduct)
#         # if updatedBillProduct.is_valid():
#         #     updatedBillProduct.save()
#         # else:
#         #     return Response(updatedBillProduct.error_messages)
 
#         # #update product
#         # oldProduct = Product.objects.get(productId =product['productId'])
#         # updatedProduct = ProductSerilizer(instance = oldProduct, data = product)
#         # if updatedProduct.is_valid():
#         #     updatedProduct.save()
#         # else:
#         #     return Response(updatedProduct.error_messages)

#     newBill = GenerateBillSerilizer(oldCustomer, many=False)
#    return Response(newBill.data)

# @api_view(['POST']) 
# def billUpdate(request):
#     # print(data)
#     oldCustomer = Customer.objects.get(customerId = request.data['customerId'])
#     print(request.data)
#     print("->>")
#     print()
#     # # print(oldCustomer)
#     # bill = Bill.objects.get()
#     # # updatedBill = UpdateExistingBillSerilizer(instance=data['customerId'], data = data)
#     updatedBill = UpdateExistingBillSerilizer(instance=oldCustomer, data = request.data)
#     print("0909")
#     if updatedBill.is_valid():
#         print("0101")
#         updatedBill.save()
#         print("0202")
#         print(updatedBill.instance)
#         # print(updatedBill.data)
#         return Response(updatedBill.data)
#     return Response(updatedBill.error_messages)BillProduct.objects.create(billId=newBill, productId=newProduct, **billProduct)

