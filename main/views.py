
from django.http.response import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from main.models import Customer, Order
from main.serializers import CustomerSerilizer, OrderSerilizer

# Create your views here.
def index(response):
    return HttpResponse("Hello from API")

#get customer with their orders
@api_view(['GET'])
def customerList(request):
    customer = Customer.objects.all()
    serializer = CustomerSerilizer(customer, many = True)

    return Response(serializer.data)


@api_view(['POST'])
#register customer with order (place order)
def placeCustomerOrder(request):
    newCustomerOrder = CustomerSerilizer(data= request.data)
    
    if newCustomerOrder.is_valid():
        newCustomerOrder.save()

        return Response(newCustomerOrder.data)
    else:
        return Response(newCustomerOrder.errors, status=status.HTTP_400_BAD_REQUEST)


# Get all order
@api_view(['GET'])
def orderList(request):
    orders = Order.objects.all()
    serializer = OrderSerilizer(orders, many = True)

    return Response(serializer.data)


## Get order by ID
@api_view(['GET'])
def order(request, pk):
    try:
        order = Order.objects.get(customerId=pk)
        serializer = OrderSerilizer(order, many=False)

        return Response(serializer.data)
    except:
        return Response({"data" : "Not Found !!"}, status=status.HTTP_404_NOT_FOUND)


# Post orders
@api_view(['POST'])
def placeOrder(request):
    newOrder = OrderSerilizer(data= request.data)

    if newOrder.is_valid():
        newOrder.save()

        return Response(newOrder.data)
    else:
        return Response(newOrder.errors, status=status.HTTP_400_BAD_REQUEST)