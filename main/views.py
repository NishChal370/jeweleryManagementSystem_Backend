from re import S
from django.db.models import Q
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import api_view #,  permission_classes
from rest_framework.pagination import PageNumberPagination
from main.models import BillProduct, Customer, Order, Bill, OrderProduct, Product, Rate, Staff, StaffWork, User
from main.serializers import AdminSerilizer, BillDetailSerilizer, BillSearchSerilizer, BillSerilizer, CustomerInfoSerilizer, CustomerOrderSerilizer, CustomerSerilizer, GenerateBillSerilizer, OrderBillSerilizer, OrderProductSerilizer, OrderSearchSerilizer, OrderSerilizer, PlaceOrderSerilizer, ProductSerilizer, RateSerilizer, StaffAssignWorkSerilizer, StaffSerilizer, StaffWorkDetailSerilizer, UpdateExistingBillSerilizer, UpdateOrderSerilizer #, send_Email, BillInfoSerilizer, BillProductInfoSerilizer

import calendar
from datetime import date, datetime, timedelta

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated   
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

##Create your views here.
def index(response):
    return HttpResponse("Hello from API")


@api_view(['POST'])
def LogoutView(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def getAdminDetail(request):
    admin = User.objects.all()
    serializer = AdminSerilizer(admin, many=True)
    return Response(serializer.data[0])


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def updateAdminDetail(request):
    oldData = User.objects.get(id=1)
    serializer = AdminSerilizer(instance=oldData, data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors)




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

        serializer = CustomerOrderSerilizer(order, many=False)

        return Response(serializer.data)
    except:
        return Response({"message" : "Not Found !!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def deleteOrder(request, pk):
    try:
        order = Order.objects.get(orderId=pk)

        if order.status != 'pending':

            return Response({"message" : "Order cannot be deleted! Is in making process."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            order.delete()

            return Response({"Order "+str(order.orderId)+" is deleted !!"}, status=status.HTTP_200_OK)
    except:
        return Response({"message" : "Not Found !!"}, status=status.HTTP_404_NOT_FOUND)



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


#update customer order
@api_view(['POST'])
def orderUpdate(request):
    oldCustomer = Customer.objects.get(customerId = request.data['customerId'])
    serilizer = UpdateOrderSerilizer(instance=oldCustomer, data=request.data)

    if serilizer.is_valid():
        serilizer.save()

        return Response(serilizer.data)

    return Response(serilizer.errors)


##Getcustomer Order
@api_view(['GET'])
def getOrders(request):
    #get only those customer who have ordered
    customers = Customer.objects.filter(customerId__in = list(Order.objects.values_list('customerId', flat=True)))
    serializer = PlaceOrderSerilizer(customers, many=True)

    return Response(serializer.data)



## GenerateOrderBill # not in use now
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
    date = request.GET.get('date')
    type = request.GET.get('type') # Query param
    status = request.GET.get('status')
    customerInfo = request.GET.get('customerInfo')
    report = request.GET.get('report')

    paginator = PageNumberPagination()
    paginator.page_size = 21

    if customerInfo != None:
        searchedCustomer = Customer.objects.filter(Q(name__icontains=customerInfo) | Q(address__icontains=customerInfo) | Q(phone__icontains=customerInfo))

    customerIdList = []
    for c in searchedCustomer:
        customerIdList.append(c.customerId)

    if len(customerIdList) >0:
        orders = Order.objects.filter(customerId__in= customerIdList)
    else:
        orders = Order.objects.all()

    if date != 'None':
        if report == 'Today':
            orders = orders.filter(submittionDate = date).order_by('submittionDate')
        else:
            orders = orders.filter(submittionDate__gte = date).order_by('submittionDate')

    if type != 'all':
        orders = orders.filter(type= type)

    if status != 'all':
        orders = orders.filter(status = status)

    if date == 'None':
        orders = orders.order_by('-date', '-orderId')

    result_page = paginator.paginate_queryset(orders, request)

    serializer = OrderSearchSerilizer(result_page, many =True)

    data = paginator.get_paginated_response(serializer.data) # current page with total page
    data.data['pageIndex'] = str(paginator.page).replace('<Page ', '').replace('>', '')

    return data



##Get order by ID
@api_view(['GET'])
def orderProductsDetail(request, pk):
    try:
        orderProducts = OrderProduct.objects.get(orderProductId = pk)
        serializer = OrderProductSerilizer(orderProducts, many=False)

        return Response(serializer.data)
    except:
        return Response({"message" : "Not Found !!"}, status=status.HTTP_404_NOT_FOUND)


##Get pending order by ID
@api_view(['GET'])
def pendingOrderProductDetail(request,orderId):
    try:

        orderProducts = OrderProduct.objects.filter(orderId = orderId).filter(status='pending')
        serializer = OrderProductSerilizer(orderProducts, many=True)
        if len(serializer.data) >0:
            return Response(serializer.data)
        else:
            return Response({"Order  work is already assigned"}, status=status.HTTP_510_NOT_EXTENDED)
    except:
        return Response({"Not Found"}, status=status.HTTP_404_NOT_FOUND)


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
    billDate = request.GET.get('billDate')
    billStatus = request.GET.get('billStatus')
    paymentStatus = request.GET.get('paymentStatus')
    # nowDate = datetime.datetime.now().date()
    nowDate = datetime.now().date()

    paginator = PageNumberPagination()
    paginator.page_size = 21

    if billDate is not None:
        bills = Bill.objects.filter(date__range = [billDate, nowDate]) #.order_by('-date', '-billId')
    else:
        bills =Bill.objects.all().order_by('-date', '-billId')


    if paymentStatus == 'remain':
        bills = bills.filter(remainingAmount__gte = 1)
    elif paymentStatus == 'payed':
        bills = bills.filter(remainingAmount__lt = 1)

    if billType != 'all': # fiter by bill type {gold, silver}
        bills = bills.filter(billType = billType) #.order_by('-date', '-billId')

    if billStatus != 'all': # fiter by bill status {submitted, draft}
        bills = bills.filter(status = billStatus) #.order_by('-date', '-billId')

    if billDate is None:
        bills = bills #.order_by('-date', '-billId')

    result_page = paginator.paginate_queryset(bills, request)

    serializer = BillSearchSerilizer(result_page, many=True)

    data = paginator.get_paginated_response(serializer.data) # current page with total page
    data.data['pageIndex'] = str(paginator.page).replace('<Page ', '').replace('>', '')

    return data



# we can search bill by name, address, phone
@api_view(['GET'])
def getBillSummaryByCustomerInfo(request, searchValue):
    billType = request.GET.get('billType') # Query param
    billDate = request.GET.get('billDate')
    billStatus = request.GET.get('billStatus')
    paymentStatus = request.GET.get('paymentStatus')

    nowDate = datetime.now().date()

    paginator = PageNumberPagination()
    paginator.page_size = 21
    searchCustomer = Customer.objects.filter(Q(name__icontains=searchValue) | Q(address__icontains=searchValue) | Q(phone__icontains=searchValue)) # __icontains  it make case insentive

    billsIdList = []
    # getting search customer bills id
    for c in searchCustomer:
        #filter by customnerId
        if billType == 'all':
            searchedBills = list(Bill.objects.filter(customerId=c).values_list('billId', flat=True))
        #filter by billType {gold, silver} & customnerId
        else:
            searchedBills = Bill.objects.filter(customerId=c).filter(billType= billType).values_list('billId', flat=True)

        billsIdList.extend(searchedBills)

    searchedBills = Bill.objects.filter(billId__in=billsIdList)

    if billDate is not None:
        searchedBills = searchedBills.filter(date__range = [billDate, nowDate])
    else:
        searchedBills =searchedBills.all()

    if billStatus != 'all':
        #fiter by bill status {submitted, draft}
        searchedBills = searchedBills.filter(status = billStatus)
    else:
        searchedBills = searchedBills.order_by('-date', '-billId')

    if paymentStatus == 'remain':
        searchedBills = searchedBills.filter(remainingAmount__gte = 1)
    elif paymentStatus == 'payed':
        searchedBills = searchedBills.filter(remainingAmount__lt = 1)

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
    if len(Rate.objects.all()) > 0 : #allow only if rate is set first
        if(Customer.objects.filter(name= request.data['name']).exists()):
            oldCustomer = Customer.objects.get(name= request.data['name'])
            newBill = GenerateBillSerilizer(instance= oldCustomer, data= request.data)
        else:
            
            newBill = GenerateBillSerilizer(data= request.data)

        if newBill.is_valid():
            newBill.save()
            return Response(newBill.data)
        else:
            return Response(newBill._errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Rate is not saved", status=status.HTTP_404_NOT_FOUND)




#Update Bill
@api_view(['POST'])
def billUpdate(request):
    if len(Rate.objects.all()) > 0 : #allow only if rate is set first
        oldCustomer = Customer.objects.get(customerId = request.data['customerId'])
        serilizer = UpdateExistingBillSerilizer(instance=oldCustomer, data=request.data)

        if serilizer.is_valid():
            serilizer.save()

            return Response(serilizer.data)

        return Response(serilizer.errors)
    else:
        return Response("Rate is not saved", status=status.HTTP_404_NOT_FOUND)



##Get customer bill
@api_view(['GET'])
def getBills(request):
    customers = Customer.objects.all()
    serializer = GenerateBillSerilizer(customers, many=True)

    return Response(serializer.data)



#Get monthly billproduct report
@api_view(['GET'])
def getMonthlyBillProductReport(request):
    month_start_date = request.GET.get('date')

    weekNumber = 0
    final_report = []
    selected_date = datetime.strptime(month_start_date, "%Y-%m-%d")

    for week in getWeekStartAndEndDate(selected_date):
        weekNumber +=1
        if len(week)>1:
            weekly_bills = Bill.objects.filter(date__range=[week[0], week[1]]).all()
        else:
            weekly_bills = Bill.objects.filter(date=week[0]).all()

        products_Id = BillProduct.objects.filter(billId__in= weekly_bills).values_list('productId', flat=True)

        products_name = Product.objects.filter(productId__in = products_Id).values_list('productName', flat=True)

        report ={'week': 'week'+str(weekNumber)}
        for product_name in products_name:
            if product_name.lower() in report :
                report[product_name.lower()] += 1
            else:
                report[product_name.lower()] = 1

        final_report.append(report)

    return Response(final_report)




@api_view(['GET'])
def getSalesReport(request):
    week_number = 0
    selected_date = datetime.strptime(request.GET.get('date') , "%Y-%m-%d")
    final_report=[]

    for week in getWeekStartAndEndDate(selected_date):
        week_number += 1
        if week[0]<=date.today():
            if len(week)>1:
                weekly_bills = Bill.objects.filter(date__range=[week[0], week[1]]).all()
            else:
                weekly_bills = Bill.objects.filter(date=week[0]).all()

            weekly_due_bills = weekly_bills.filter(remainingAmount__gt =0).all()
            weekly_payed_bills = weekly_bills.filter(remainingAmount__lte =0).all()

            due_amount = 0
            payed_amount = 0
            total_amount = 0
            for bill in weekly_due_bills:
                due_amount += bill.remainingAmount
            for bill in weekly_payed_bills:
                payed_amount += bill.payedAmount
            for bill in weekly_bills:
                total_amount += bill.grandTotalAmount

            report={'week' :'week '+str(week_number),'report' :{'total amount' :total_amount,'due amount' :due_amount, 'payed amount': payed_amount}}
            # report = {'total amount' :total_amount,'due amount' :due_amount, 'payed amount': payed_amount}
            final_report.append(report)

    labels = []
    datas={'total amount' :[], 'payed amount' :[], 'due amount' :[],}
    for report in final_report:
        labels.append(report['week'])
        datas['due amount'].append(report['report']['due amount'])
        datas['total amount'].append(report['report']['total amount'])
        datas['payed amount'].append(report['report']['payed amount'])

    return Response({'labels':labels, 'report': datas})


# bill, order, staffwork total and increment of this month Report
@api_view(['GET'])
def getIncrementReport(request):
    this_month_first_date = datetime.today().replace(day=1).date()
    this_month_last_day = calendar.monthrange(this_month_first_date.year, this_month_first_date.month)[1]
    this_month_last_date = datetime.today().replace(day=this_month_last_day).date()

    previous_month_first_date = datetime.today().replace(month=this_month_first_date.month-1, day=1).date()
    previous_month_last_day = calendar.monthrange(previous_month_first_date.year, previous_month_first_date.month)[1]
    previous_month_last_date = datetime.today().replace(month=this_month_first_date.month-1, day=previous_month_last_day).date()
    #bill
    this_month_bills = Bill.objects.filter(date__range=[this_month_first_date, this_month_last_date]).all()
    previous_month_bills = Bill.objects.filter(date__range=[previous_month_first_date, previous_month_last_date]).all()

    this_month_total_bill = len(this_month_bills)
    previous_month_total_bill = len(previous_month_bills)

    if (this_month_total_bill+previous_month_total_bill == 0 ): # if no bill exist 
        bill_increment_percent = 0
    else:
        bill_increment_percent = ((this_month_total_bill-previous_month_total_bill)/(this_month_total_bill+previous_month_total_bill))*100

    #order
    this_month_orders = Order.objects.filter(date__range=[this_month_first_date, this_month_last_date]).all()
    previous_month_orders = Order.objects.filter(date__range=[previous_month_first_date, previous_month_last_date]).all()

    this_month_total_order = len(this_month_orders)
    previous_month_total_order = len(previous_month_orders)

    if ( this_month_total_order+previous_month_total_order == 0 ): # if no order exist 
        order_increment_percent = 0
    else:
        order_increment_percent = ((this_month_total_order-previous_month_total_order)/(this_month_total_order+previous_month_total_order))*100
    
    #order
    this_month_staffworks = StaffWork.objects.filter(date__range=[this_month_first_date, this_month_last_date]).all()
    previous_month_staffworks = StaffWork.objects.filter(date__range=[previous_month_first_date, previous_month_last_date]).all()

    this_month_total_staffwork = len(this_month_staffworks)
    previous_month_total_staffwork = len(previous_month_staffworks)

    if ( this_month_total_staffwork+previous_month_total_staffwork == 0): # if no staff exist 
        staffwork_increment_percent = 0
    else:
        staffwork_increment_percent = ((this_month_total_staffwork-previous_month_total_staffwork)/(this_month_total_staffwork+previous_month_total_staffwork))*100

    report={ 'bill':{'total':this_month_total_bill, 'increment':str(int(round(bill_increment_percent)))+'%'},
            'order':{'total':this_month_total_order, 'increment':str(int(round(order_increment_percent)))+'%'},
            'staffWork':{'total':this_month_total_staffwork, 'increment':str(int(round(staffwork_increment_percent)))+'%'},}

    return Response(report)


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
    existingRate = Rate.objects.filter(date= datetime.now())

    if(existingRate.exists()):

        oldRate = Rate.objects.get(date= datetime.now())
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




## GET Rate report
@api_view(['GET'])
def getRateReport(request):
    reportType = request.GET.get('type')
    # dayIndex = {6:0, 0:1, 1:2, 2:3, 3:4, 4:5, 5:6}
    rates = Rate.objects.all()

    if reportType == 'weekly':
        todays_day_index =datetime.today().isoweekday()

        week_start_date = datetime.today() - timedelta(days= todays_day_index) if todays_day_index != 7 else datetime.today()
        week_end_date = week_start_date + timedelta(days=6)

        rates = Rate.objects.filter(date__range=[week_start_date, week_end_date])

        rateWeeklyRateList=[]
        serializer = RateSerilizer(rates, many=True).data
        for data in serializer:
            rateWeeklyRateList.append({"index":data['date'], 'hallmarkRate' :(data['hallmarkRate'])/1000, 'tajabiRate' :(data['tajabiRate'])/1000, 'silverRate': (data['silverRate'])/100})

        return Response(rateWeeklyRateList)

    elif reportType == 'monthly':
        weekCount = 0
        rateWeeklyRateList= []
        for week in getWeekStartAndEndDate(datetime.today()):
            weekCount += 1

            if len(week)>1:
                serilizer = RateSerilizer(Rate.objects.filter(date__range=[week[0], week[1]]), many=True).data
            else:
                serilizer = RateSerilizer(Rate.objects.filter(date=week[0]), many=True).data # added .data clz when data is 1 then "TypeError: 'ListSerializer' object is not iterable" occured

            if serilizer != []:
                tajabiRateTotal = 0.0
                silverRateTotal = 0.0
                hallmarkRateTotal =0.0
                for data in serilizer:
                    tajabiRateTotal += data['tajabiRate']
                    silverRateTotal += data['silverRate']
                    hallmarkRateTotal += data['hallmarkRate']

                rateWeeklyRateList.append({"index":'week '+str(weekCount), 'avgHallmarkRate' :(hallmarkRateTotal/len(serilizer))/1000, 'avgTajabiRate' :(tajabiRateTotal/len(serilizer))/1000, 'avgSilverRate': (silverRateTotal/len(serilizer))/100})

        return Response(rateWeeklyRateList)

    elif reportType == 'yearly':
        month = 0
        monthList = []
        while month < 12:
            month += 1
            month_start_date = datetime.now().replace(month=month, day=1).date()
            month_last_day = calendar.monthrange(month_start_date.year, month_start_date.month)[1]

            month_end_date = datetime.now().replace(month=month,day=month_last_day).date()

            monthList.append([month_start_date, month_end_date])

        rateYearlyRateList= []
        for month in monthList:
            serilizer = RateSerilizer(Rate.objects.filter(date__range=[month[0], month[1]]), many=True).data

            if serilizer != []:
                tajabiRateTotal = 0.0
                silverRateTotal = 0.0
                hallmarkRateTotal =0.0
                for data in serilizer:
                    tajabiRateTotal += data['tajabiRate']
                    silverRateTotal += data['silverRate']
                    hallmarkRateTotal += data['hallmarkRate']

                rateYearlyRateList.append({"index":month[0].strftime("%B"), 'avgHallmarkRate' :(hallmarkRateTotal/len(serilizer))/1000, 'avgTajabiRate' :(tajabiRateTotal/len(serilizer))/1000, 'avgSilverRate': (silverRateTotal/len(serilizer))/100})

        return Response(rateYearlyRateList)





def getWeekStartAndEndDate(date):
    month_first_date = date.replace(day=1).date()
    month_last_day = calendar.monthrange(month_first_date.year, month_first_date.month)[1]
    month_last_date = date.replace(day=month_last_day).date()
    tempList =[]
    weekDayList =[]
    tempDate = month_first_date
    while tempDate.month == month_first_date.month:
        tempList.append(tempDate)
        if tempDate.weekday() == 5:
            day = 1

            weekDayList.append(tempList)
            tempList =[]
        elif tempDate.weekday() == 6:
            day =6
        else:
            day = 5-tempDate.weekday()# int value range: 0-6, monday-sunday

        tempDate = tempDate + timedelta(days= day)

    tempList.append(month_last_date)
    weekDayList.append(tempList)
    tempList =[]

    return weekDayList


'''
 # Staff
'''

#GET staff Detail
@api_view(['GET'])
def getStaffDetail(request):
    staffs = Staff.objects.all()
    serializer = StaffSerilizer(staffs, many=True)

    return Response(serializer.data)



#GET staffs name list
@api_view(['GET'])
def getStaffNameList(request):
    staffs = Staff.objects.all().values('staffId', 'staffName')
    if len(staffs)>0:
        return Response(staffs)
    else:
        return Response({"No staff Registered"}, status=status.HTTP_404_NOT_FOUND)





#Register staff
@api_view(['POST'])
def registerStaff(request):
    if(Staff.objects.filter(phone= request.data['phone']).exists()):

        return Response(request.data['staffName']+' is already registed !!', status.HTTP_406_NOT_ACCEPTABLE)
    else:
        newStaff = StaffSerilizer(data= request.data)

    if newStaff.is_valid():
        newStaff.save()
        #return all staff
        allStaffs = Staff.objects.all()
        serializer = StaffSerilizer(allStaffs, many=True)
        return Response(serializer.data)
    else:
        return Response(newStaff.errors, status=status.HTTP_400_BAD_REQUEST)



#update staff by id
@api_view(['POST'])
def updateStaffById(request, pk):
    try:
        oldStaff =  Staff.objects.get(staffId= pk)

        updatedStaff = StaffSerilizer(instance=oldStaff, data=request.data)
        if updatedStaff.is_valid():
            updatedStaff.save()
            #returFn all staff
            allStaffs = Staff.objects.all()
            serializer = StaffSerilizer(allStaffs, many=True)
            return Response(serializer.data)
        else:
            return Response(updatedStaff.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Invalid !!!"}, status=status.HTTP_400_BAD_REQUEST)



#delete bill by id----------------
@api_view(['DELETE'])
def deleteStaffById(request, pk):
    try:
        staff = Staff.objects.get(staffId=pk)

        staffSerilizer = StaffSerilizer(staff, many=False)

        if staffSerilizer.data['inprogress'] <=0 :
            staff.delete()
            # Staff.objects.filter(staffId=pk).update(resignDate = datetime.date.today())
            staff = Staff.objects.all()
            staff = StaffSerilizer(staff, many=True)
            return Response(staff.data)
        else:
            return Response({staffSerilizer.data['staffName']+" have work to complete"}, status=status.HTTP_428_PRECONDITION_REQUIRED)

    except:
        return Response({"message" : "Not Found !!"}, status=status.HTTP_404_NOT_FOUND)



#delete bill by id
@api_view(['GET'])
def getStaffbyId(request, pk):
    try:
        staff = Staff.objects.get(staffId=pk)

        staffSerilizer = StaffSerilizer(staff, many=False)

        return Response(staffSerilizer.data)
    except:
        return Response({"message" : "Not Found !!"}, status=status.HTTP_404_NOT_FOUND)



#GET staff work detail
@api_view(['GET'])
def getStaffWorkDetail(request):
    type = request.GET.get('type') # Query param
    orderId = request.GET.get('orderId')
    staffInfo = request.GET.get('staffInfo')
    workStatus = request.GET.get('workStatus')
    submittionDate = request.GET.get('submittionDate')
    report = request.GET.get('report')

    paginator = PageNumberPagination()
    paginator.page_size = 21

    if submittionDate != '':
        if report == 'Today':
            staffWork = StaffWork.objects.filter(submittionDate = submittionDate).order_by('submittionDate').all()
        else:
            staffWork = StaffWork.objects.filter(submittionDate__gte = submittionDate).order_by('submittionDate').all()
    else:
        staffWork = StaffWork.objects.all()

    if staffInfo != '': #
        searchedStaff = Staff.objects.filter(Q(staffName__icontains=staffInfo) |  Q(phone__icontains=staffInfo))
        staffWork = staffWork.filter(staff__in = searchedStaff).all()

    if orderId != '':
        searchedOrder = Order.objects.get(orderId=orderId)
        orderProduct = OrderProduct.objects.filter(orderId=searchedOrder).all()

        staffWork = staffWork.filter(orderProduct__in = orderProduct).all()

    if workStatus != '':
        staffWork = staffWork.filter(status = workStatus).all()

    if type != '':
        searchedOrder = Order.objects.filter(type=type)
        orderProduct = OrderProduct.objects.filter(orderId__in =searchedOrder).all()

        staffWork = staffWork.filter(orderProduct__in = orderProduct).all()

    if submittionDate == '':
        staffWork = staffWork.order_by('-date', '-staffWorkId')

    result_page = paginator.paginate_queryset(staffWork, request)
    serilizer =StaffWorkDetailSerilizer(result_page, many=True)

    data = paginator.get_paginated_response(serilizer.data) # current page with total page
    data.data['pageIndex'] = str(paginator.page).replace('<Page ', '').replace('>', '')

    return data




#Assign work to staff
@api_view(['POST'])
def assignStaffWork(request):
    workDetail = request.data

    if workDetail['staffWorkId'] != None:
        oldWork = StaffWork.objects.get(staffWorkId = workDetail['staffWorkId'])

        newWork = StaffAssignWorkSerilizer(instance=oldWork, data=workDetail)
    else:
        newWork = StaffAssignWorkSerilizer(data= workDetail)

    if newWork.is_valid():
        newWork.save()

        return Response(newWork.data)
    else:
        return Response(newWork.error_messages, status=status.HTTP_404_NOT_FOUND)



'''
 #Customer
'''
@api_view(['GET'])
def getCustomerReport(request):
    customers = Customer.objects.all()

    addressDetail= {}
    for customer in customers:
        if customer.address.lower() in addressDetail:
            addressDetail[customer.address.lower()] += 1
        else:
            addressDetail[customer.address.lower()] = 1

    return Response(addressDetail)



class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)