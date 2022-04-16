from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from main.tests.tests_auth import authenticate
from main.models import Customer, Order, OrderProduct, Product, Rate


class TestOrder(APITestCase):
      def setUp(self):
            rate = Rate.objects.create(
                  hallmarkRate = 90000, 
                  tajabiRate = 89000, 
                  silverRate = 1600
            )
            customer = Customer.objects.create(
                  name = "Hari",
                  address = "nepal",
                  phone = "9805169542",
                  email = "np01cp4a190072@islingtoncollege.edu.np"
            )
            order = Order.objects.create(
                  date = date.today(),
                  customerId = customer,
                  submittionDate = "2022-04-05",
                  type = 'gold',
                  status = 'pending',
            )
            product = Product.objects.create(
                  productName = 'ring',
                  netWeight = 14,
                  gemsName = 'muga',
                  gemsPrice = 1500
            )
            orderProduct = OrderProduct.objects.create(
                  orderId = order,
                  productId = product,
                  status = 'pending',
            )

      def test_get_orders(self):
            authenticate(self)

            response = self.client.get(reverse('orders-list'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data[0]['name'], 'Hari')
            self.assertEqual(type(response.data[0]['orders']), list)
            self.assertTrue('orderProducts' in response.data[0]['orders'][0])
            self.assertTrue('product' in response.data[0]['orders'][0]['orderProducts'][0])
      #done
      def test_place_order(self):
            authenticate(self)

            data ={
                  'name' : "Hari",
                  'address' : "nepal",
                  'phone' : "9805169542",
                  'email' : "np01cp4a190072@islingtoncollege.edu.np",
                  'orders' :[{
                        'date' : date.today(),
                        'submittionDate' : "2022-04-05",
                        'type' : 'silver',
                        'status' : 'pending',
                        'orderProducts':[{
                              'status' :'pending',
                              'product':{
                                    'productName' : 'earring',
                                    'netWeight' : 14,
                                    'gemsName' : 'mooti',
                                    'gemsPrice' : 1500
                              }
                        }]

                  }]
            }

            response = self.client.post('/api/place-order/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['name'], 'Hari')
            self.assertTrue('orders' in response.data)
            self.assertTrue('orderProducts' in response.data['orders'][1])
            self.assertTrue('product' in response.data['orders'][1]['orderProducts'][0])
      #done
      def test_place_order_without_order(self):
            authenticate(self)

            data ={
                  'name' : "Hari",
                  'address' : "nepal",
                  'phone' : "9805169542",
                  'email' : "np01cp4a190072@islingtoncollege.edu.np",
            }

            response = self.client.post('/api/place-order/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['message'][0], 'Order is missing.')
      #done
      def test_update_order(self):
            authenticate(self)

            todays_gold_rate = Rate.objects.get(date= date.today()).hallmarkRate
            data ={
                  'customerId' : 1,
                  'name' : "Hari",
                  'address' : "nepal",
                  'phone' : "9805169542",
                  'email' : "np01cp4a190072@islingtoncollege.edu.np",
                  'orders' :[{
                        'orderId' : 1,
                        'date' : date.today(),
                        'submittionDate' : "2022-04-06",
                        'type' : 'gold',
                        'rate': todays_gold_rate,
                        'status' : 'pending',
                        'orderProducts':[{
                              'orderProducts' : 1,
                              'status' :'pending',
                              'product':{
                                    'productId':2,
                                    'productName' : 'earring',
                                    'netWeight' : 30,
                                    'gemsName' : 'mooti',
                                    'gemsPrice' : 4000
                              }
                        }]

                  }]
            }

            response = self.client.post('/api/order/update', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['orders'][0]['rate'], 90000)
            self.assertTrue('product' in response.data['orders'][0]['orderProducts'][0]) 
      #done
      def test_update_submitted_order(self):
            authenticate(self)

            todays_gold_rate = Rate.objects.get(date= date.today()).hallmarkRate
            data ={
                  'customerId' : 1,
                  'name' : "Hari",
                  'address' : "nepal",
                  'phone' : "9805169542",
                  'email' : "np01cp4a190072@islingtoncollege.edu.np",
                  'orders' :[{
                        'orderId' : 1,
                        'date' : date.today(),
                        'submittionDate' : "2022-04-06",
                        'submittedDate' : "2022-04-06",
                        'type' : 'gold',
                        'rate': todays_gold_rate,
                        'status' : 'submitted',
                        'orderProducts':[{
                              'orderProducts' : 1,
                              'status' :'submitted',
                              'product':{
                                    'productId':2,
                                    'productName' : 'earring',
                                    'netWeight' : 30,
                                    'gemsName' : 'mooti',
                                    'gemsPrice' : 4000
                              }
                        }]

                  }]
            }

            response = self.client.post('/api/order/update', data, format='json')
            self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue(response.data, 'Order already submitted')   
      #done
      def test_update_inprogress_order(self):
            authenticate(self)

            todays_gold_rate = Rate.objects.get(date= date.today()).hallmarkRate
            data ={
                  'customerId' : 1,
                  'name' : "Hari",
                  'address' : "nepal",
                  'phone' : "9805169542",
                  'email' : "np01cp4a190072@islingtoncollege.edu.np",
                  'orders' :[{
                        'orderId' : 1,
                        'date' : date.today(),
                        'submittionDate' : "2022-04-06",
                        'submittedDate' : "2022-04-06",
                        'type' : 'gold',
                        'rate': todays_gold_rate,
                        'status' : 'inprogress',
                        'orderProducts':[{
                              'orderProducts' : 1,
                              'status' :'inprogress',
                              'product':{
                                    'productId':2,
                                    'productName' : 'earring',
                                    'netWeight' : 30,
                                    'gemsName' : 'mooti',
                                    'gemsPrice' : 4000
                              }
                        }]

                  }]
            }

            response = self.client.post('/api/order/update', data, format='json')
            self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue(response.data, 'Order inprogress')

      def test_delete_order_by_id(self):
            authenticate(self)

            response = self.client.delete('/api/order-delete/1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, {'Order 1 is deleted'})       
      #done
      def test_get_order_summary(self):
            authenticate(self)
            # by date
            response = self.client.get('/api/orders/summary/?customerInfo=None&type=all&status=all&date=2022-04-04&page=1') 
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['results'][0]['date'], '2022-04-04')  
            # by name
            response = self.client.get('/api/orders/summary/?customerInfo=Hari&type=all&status=all&date=None&page=1') 
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['results'][0]['customerName'], 'Hari') 
            # by type
            response = self.client.get('/api/orders/summary/?customerInfo=None&type=gold&status=all&date=None&page=1') 
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['results'][0]['type'], 'gold') 
            # not found
            response = self.client.get('/api/orders/summary/?customerInfo=None&type=silver&status=all&date=None&page=1') 
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['results'], []) 

      def test_get_by_id(self):
            authenticate(self)

            response = self.client.get('/api/order/1') 
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['orders']['orderId'], 1)

            response = self.client.get('/api/order/2') 
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

      def test_get_order_product_by_id(self):
            authenticate(self)

            response = self.client.get('/api/orderProduct/1') 
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['orderProductId'], 1)

            response = self.client.get('/api/orderProduct/2') 
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
      