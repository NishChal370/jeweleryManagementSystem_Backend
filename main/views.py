
from math import e
from django.http.response import HttpResponse

from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import api_view

import datetime
from django.utils.timezone import now

from main.models import Customer, Order, Bill, Product, Rate
from main.serializers import BillSearchSerilizer, BillSerilizer, CustomerInfoSerilizer, CustomerSerilizer, GenerateBillSerilizer, OrderBillSerilizer, OrderSerilizer, PlaceOrderSerilizer, ProductSerilizer, RateSerilizer

from rest_framework.pagination import PageNumberPagination
#Q objects that allow to complex lookups.
from django.db.models import Q
##Create your views here.
def index(response):
    return HttpResponse("Hello from API")



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
@api_view(['POST'])
def placeOrder(request):
    newOrder = OrderSerilizer(data= request.data)

    if newOrder.is_valid():
        newOrder.save()

        return Response(newOrder.data)
    else:
        return Response(newOrder.errors, status=status.HTTP_400_BAD_REQUEST)



##Get all bills
@api_view(['GET'])
def billsList(request): 
    bills = Bill.objects.all()
    serializer = BillSerilizer(bills, many=True)

    return Response(serializer.data)


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


##Get bill summary / bill search in frontend
@api_view(['GET'])
def billsListSummmary(request):
    billType = request.GET.get('billType') # Query param

    paginator = PageNumberPagination()
    paginator.page_size = 21

    if(billType != 'all'):
        bills = Bill.objects.filter(billType = billType)
    else:
        bills = Bill.objects.all()

    bills = bills.order_by('-date', '-billId')

    result_page = paginator.paginate_queryset(bills, request)

    serializer = BillSearchSerilizer(result_page, many=True)

    data = paginator.get_paginated_response(serializer.data)
    data.data['pageIndex'] = str(paginator.page).replace('<Page ', '').replace('>', '')

    return data


'''
    # we can search bill by name, address, phone
'''
@api_view(['GET'])
def getBillSummaryByName(request, searchValue):
    billType = request.GET.get('billType') # Query param

    paginator = PageNumberPagination()
    paginator.page_size = 21
    searchCustomer = Customer.objects.filter(Q(name__icontains=searchValue) | Q(address__icontains=searchValue) | Q(phone__icontains=searchValue)) # __icontains  it make case insentive

    billsIdList = []
    for c in searchCustomer:# getting search customer bills id
        if(billType == 'all'):
            # billsIdList.extend(list(Bill.objects.filter(customerId=c).values_list('billId', flat=True)))
            searchedBills = list(Bill.objects.filter(customerId=c).values_list('billId', flat=True))
        else:
            # billsIdList.extend(Bill.objects.filter(customerId=c).filter(billType= billType).values_list('billId', flat=True))
            searchedBills = Bill.objects.filter(customerId=c).filter(billType= billType).values_list('billId', flat=True)
        billsIdList.extend(searchedBills)
        

    filteredBills = Bill.objects.filter(billId__in=billsIdList).order_by('-date', '-billId')

    result_page = paginator.paginate_queryset(filteredBills, request)

    serializer = BillSearchSerilizer(result_page, many=True)

    data = paginator.get_paginated_response(serializer.data)
    data.data['pageIndex'] = str(paginator.page).replace('<Page ', '').replace('>', '')

    return data    



##Get bill by ID
@api_view(['GET'])
def billById(request, pk):
    try:
        bill = Bill.objects.get(billId=pk)
        serializer = BillSerilizer(bill, many=False)

        return Response(serializer.data)
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



##Get customer bill
@api_view(['GET'])
def getBills(request):
    customers = Customer.objects.all()
    serializer = GenerateBillSerilizer(customers, many=True)

    return Response(serializer.data)



##Generate Order
@api_view(['POST'])
def generateOrder(request):

    if(Customer.objects.filter(name= request.data['name']).exists()):
        oldCustomer = Customer.objects.get(name= request.data['name'])
        newOrder = PlaceOrderSerilizer(instance= oldCustomer, data= request.data)
    else:
        newOrder = PlaceOrderSerilizer(data= request.data)

    if newOrder.is_valid():
        newOrder.save()

        return Response(newOrder.data)
    else:
        
        return Response(newOrder.errors, status=status.HTTP_400_BAD_REQUEST)



##Getcustomer Order
@api_view(['GET'])
def getOrders(request):
    customers = Customer.objects.all()
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