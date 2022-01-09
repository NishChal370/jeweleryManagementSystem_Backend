from django.urls.conf import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('customers/', views.customerList, name='customers-list'),
    path('place-customer-order-bill/', views.placeCustomerOrderOrBill, name='customer-order-bill'),
    
    path('orders/',views.orderList, name='orders'),
    path('order/<int:pk>', views.order, name='order'),
    path('order-place/', views.placeOrder, name='place-order'),

    path('bills/', views.billsList, name='bill-list'), 

    path('products/', views.productList, name='product-list'), 

    path('generate-bill/', views.generateBill, name='generate-bill'),
    path('place-order/', views.generateOrder, name='place-order'),

    path('bills-list/',views.getBills, name='bills-list'),
    path('orders-list/',views.getOrders, name='orders-list'),
    path('generate-order-bill/', views.generateOrderBill, name='enerate-order-bill'),

    path('rates/', views.getAllRates, name='rates-list'),
    path('rate-set/', views.setRate, name='rate-set'),
    path('rate/<str:date>', views.getRateByDate, name='rate-by-date'),
    path('rate-update/<int:pk>', views.updateTodaysRate, name='rate-update'),
]

