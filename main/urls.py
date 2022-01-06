from django.urls.conf import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('customers/', views.customerList, name='customers-list'),
    path('place-customer-order/', views.placeCustomerOrder, name='customer-order'),
    
    path('orders/',views.orderList, name='orders-list'),
    path('order/<int:pk>', views.order, name='order'),
    path('order-place/', views.placeOrder, name='place-order'),

    path('bills/', views.billsList, name='bill-list'), 
]

