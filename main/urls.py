from django.urls.conf import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('place-customer-order-bill/', views.placeCustomerOrderOrBill, name='customer-order-bill'),


    #Customer
    path('customers/', views.customerList, name='customers-list'),
    path('customer/<int:pk>', views.customerById, name='customer-by-id'),
    
    
    ## Orders
    path('orders/',views.orderList, name='orders'),
    path('order/<int:pk>', views.order, name='order'),
    path('orders/summary/',views.orderListSummary, name='orders-list-summary'),
    path('orders-list/',views.getOrders, name='orders-list'),
    # # path('order-place/', views.placeOrder, name='place-order'),
    path('place-order/', views.generateOrder, name='place-order'),
    path('generate-order-bill/', views.generateOrderBill, name='generate-order-bill'),


    ## Bills
    path('bills/', views.billsList, name='bill-list'),
    path('bills-list/',views.getBills, name='bills-list'), 
    path('bill/<int:pk>', views.billById, name='bill-by-id'),
    path('bill/update', views.billUpdate, name='update-bill-by-id'),
    path('generate-bill/', views.generateBill, name='generate-bill'),
    path('bills/summary/', views.billsListSummmary, name='bill-list-summmary'), 
    path('bill/delete/<int:pk>', views.deleteBillById, name='bill-delete-by-id'),
    path('bills/summary/<str:searchValue>/', views.getBillSummaryByCustomerInfo, name='bill-list-summmary-name'), 
    

    #Products
    path('products/', views.productList, name='product-list'), 


    #Rate
    path('rates/', views.getAllRates, name='rates-list'),
    path('rate-set/', views.setRate, name='rate-set'),
    path('rate/<str:date>', views.getRateByDate, name='rate-by-date'),
    path('rate-update/<int:pk>', views.updateTodaysRate, name='rate-update'),
]