
from django.http.response import HttpResponse

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.utils import serializer_helpers


from main.models import Customer, Order, Bill, Product
from main.serializers import BillSerilizer, CustomerSerilizer, GenerateBillSerilizer, OrderBillSerilizer, OrderSerilizer, PlaceOrderSerilizer, ProductSerilizer

##Create your views here.
def index(response):
    return HttpResponse("Hello from API")

##Get customer with their orders and bills
@api_view(['GET'])
def customerList(request):
    customer = Customer.objects.all()
    serializer = CustomerSerilizer(customer, many = True)

    return Response(serializer.data)


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
        order = Order.objects.get(customerId=pk)
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
    #newBill = GenerateBillSerilizer(data=request.data)

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