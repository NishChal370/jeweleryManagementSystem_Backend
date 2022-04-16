from datetime import date
from django.urls import reverse
from rest_framework import status
from asyncio.windows_events import NULL
from rest_framework.test import APITestCase
from main.tests.tests_auth import authenticate
from main.models import Bill, BillProduct, Customer, Order, OrderProduct, Product, Rate, Staff, StaffWork



class TestBill(APITestCase):
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
            bill = Bill.objects.create(
                  customerId = customer,
                  date = "2022-01-08",
                  rate = 500.0,
                  billType = 'gold',
                  customerProductWeight = NULL,
                  customerProductAmount = NULL,
                  finalWeight = 14, 
                  grandTotalWeight = 490.0, 
                  totalAmount = 500.0,
                  discount = 10.0,
                  grandTotalAmount =  490.0,
                  advanceAmount = NULL,
                  payedAmount = 490.0,
                  remainingAmount = NULL,
                  status = "submitted",
                  qr_code = 'img.jpg',
            )
            product = Product.objects.create(
                  productName = 'ring',
                  netWeight = 12,
                  size = NULL,
                  gemsName = 'muga',
                  gemsPrice = 1500,
            )
            BillProduct.objects.create(
                  billId = bill,
                  productId = product,
                  lossWeight = 0.0,
                  totalWeight = 14,
                  quantity = 1,
                  rate = rate.hallmarkRate,
                  makingCharge = 500,
                  totalAmountPerProduct = 13100,
            )

            staff =  Staff.objects.create(
                  staffName = "ankit",
                  address = "Beni",
                  phone = "9878764857",
                  email = NULL,
                  registrationDate = "2022-02-15"
            )
            #place order
            order = Order.objects.create(
                  customerId = customer,
                  date = date.today(),
                  rate = rate.hallmarkRate,
                  advanceAmount = 0,
                  submittionDate = date.today(),
                  # submittedDate = '',
                  remark = '',
                  customerProductWeight = 0,
                  type = 'gold',
                  status = 'inprogress'
            )
            prooduct = Product.objects.create(
                  productName = 'ring',
                  netWeight = 14,
                  size = 23,
                  gemsName = 'muga',
                  gemsPrice = 1500,
            )
            order_product = OrderProduct.objects.create(
                  orderId = order,
                  productId = prooduct,
                  totalWeight = 14,
                
                  status = 'inprogress',
            )
            #work to staff
            staff_work = StaffWork.objects.create(
                  staff = staff,
                  orderProduct = order_product,
                  date = date.today(), #"2022-02-15"
                  givenWeight = 14,
                  KDMWeight = 5,
                  totalWeight = 19,
                  submittionDate = date.today(),
                  submittedWeight = NULL,
                  finalProductWeight = NULL,
                  lossWeight = 0,
                  # submittedDate = NULL,
                  status = 'inprogress',
            )
            StaffWork.objects.update(
                  staff = staff,
                  KDMWeight = 5,
                  date = date.today(),
                  finalProductWeight = 19,
                  givenWeight = 14,
                  lossWeight = 0,
                  orderProduct = order_product,
                  # staffWorkId =  staff_work,
                  status = "completed",
                  submittedDate = date.today(),
                  submittedWeight = 19,
                  submittionDate = date.today(),
                  totalWeight = 19,
            )

      def test_get_bill_no_auth(self):
            response = self.client.get(reverse('bills-list'))

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

      def test_get_bill(self):
            authenticate(self)
            
            response = self.client.get(reverse('bills-list'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, list)
            self.assertTrue('bills' in response.data[0])
            self.assertTrue('customerId' in response.data[0])
            self.assertTrue('billProduct' in response.data[0]['bills'][0])
            self.assertTrue(response.data[0]['bills'][0]['billProduct'], list)
            self.assertTrue('product' in response.data[0]['bills'][0]['billProduct'][0])
            self.assertTrue(response.data[0]['bills'][0]['billProduct'][0]['product'], dict)
            

      def test_get_bill_by_id(self):
            authenticate(self)
            
            response = self.client.get('/api/bill/1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(1, response.data['billId'])
      
      def test_delete_bill_by_id(self):
            authenticate(self)
            
            response = self.client.delete('/api/bill/delete/2')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response = self.client.delete('/api/bill/delete/2')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertTrue(response.data['message'], 'Not Found !!')
      

      #done
      def test_get_bills_summary(self):
            authenticate(self)

            response = self.client.get(reverse('bill-list-summmary'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
      #done
      def test_bill_summary_filter(self):
            authenticate(self)

            response = self.client.get('/api/bills/summary/Hari/?billType=all&billStatus=all&page=1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue('results', response.data)
            self.assertTrue('Hari', response.data['results'][0]['customerName'])

            response = self.client.get('/api/bills/summary/Hari/?billType=gold&billDate=2022-01-08&billStatus=submitted&page=1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue('results', response.data)
            self.assertTrue('gold', response.data['results'][0]['type'])
            self.assertTrue('2022-01-08', response.data['results'][0]['date'])
            self.assertTrue('submitted', response.data['results'][0]['status'])

            response = self.client.get('/api/bills/summary/Hari/?billType=gold&billDate=2022-01-08&billStatus=submitted&page=2')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

            response = self.client.get('/api/bills/summary/Sonam/?billType=all&billStatus=all&page=1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue('results', response.data)

            response = self.client.get('/api/bills/summary/?paymentType=payed')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response = self.client.get('/api/bills/summary/?paymentType=remain')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

      #done
      def test_generate_bill(self):
            authenticate(self)
            data = {
                  'name': 'Ganga', 
                  'address': 'beni', 
                  'phone': '9878276456', 
                  'email': '', 
                  'bills': [{ 
                        'advanceAmount': NULL,
                        'billType': "gold",
                        'customerProductAmount': 0,
                        'customerProductWeight': 0,
                        'date': "2022-04-03",
                        'discount': NULL,
                        'finalWeight': 44,
                        'grandTotalAmount': 44620,
                        'grandTotalWeight': 44,
                        'payedAmount': NULL,
                        'rate': 98000,
                        'remainingAmount': 44620,
                        'status': "draft",
                        'totalAmount': 44620,
                        'billProduct': [{
                              'lossWeight': "4",
                              'makingCharge': "1500",
                              'quantity': 1,
                              'rate': 98000,
                              'totalAmountPerProduct': 44620,
                              'totalWeight': 44,
                              'product': {
                                    'productName': 'neckles', 
                                    'netWeight': '40', 
                                    'size': 0, 
                                    'gemsName': '', 
                                    'gemsPrice': NULL,
                              }
                        }]
                  }]
                  
            }
            response = self.client.post('/api/generate-bill/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['name'], 'Ganga')
            self.assertTrue('bills' in response.data)
            self.assertTrue('billProduct' in response.data['bills'][0])
            self.assertTrue('product' in response.data['bills'][0]['billProduct'][0])

      #done
      def test_missing_bill(self):
            authenticate(self)
            data ={
                  "name":"gopal",
                  "address":"kathmandu",
                  "phone":"9878767654",
                  "email":"gopal@gmail.com",
            }

            response = self.client.post('/api/generate-bill/', data,  format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue(response.data['message'][0], 'Bill is missing')
      #done
      def test_update_bill(self):
            authenticate(self)

            rate = Rate.objects.get(date= date.today())
            data = {
                  "customerId": 1,
                  "email": "",
                  "name": "Kiraaan",
                  "phone": "9856425168",
                  "address": "America",
                  "bills": [
                        {
                        "billId":1,
                        "customerProductAmount": 0,
                        "customerProductWeight": 0,
                        "date": "2022-01-30",
                        "discount": NULL,
                        "finalWeight": 107,
                        "grandTotalAmount": 196088,
                        "grandTotalWeight": 107,
                        "payedAmount": NULL,
                        "rate": rate.hallmarkRate,
                        "remainingAmount": 196088,
                        "status": "draft",
                        "totalAmount": 196088,
                        "advanceAmount": NULL,
                        "billProduct": [
                              {
                                    "billProductId": 1,
                                    "billId": 1,
                                    "lossWeight": 9,
                                    "makingCharge": 900,
                                    "quantity": 1,
                                    "rate": 90000,
                                    "totalAmountPerProduct": 196088,
                                    "totalWeight": NULL,
                                    "product":{
                                    "gemsName": "dimond",
                                    "gemsPrice": 98888,
                                    "netWeight": 98,
                                    "productId": 1,
                                    "productName": "Bala",
                                    "size": 0
                                    }
                              }
                        ]
                        }
                  ]
            }

            response = self.client.post('/api/bill/update', data,  format='json')
            self.assertTrue(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['name'], 'Kiraaan')
            self.assertTrue(response.data['address'], 'America')
      #done
      def test_update_bill_submitted(self):
            authenticate(self)

            rate = Rate.objects.get(date= date.today())
            data = {
                  "customerId": 1,
                  "email": "",
                  "name": "Kiraaan",
                  "phone": "9856425168",
                  "address": "America",
                  "bills": [
                        {
                        "billId":1,
                        "customerProductAmount": 0,
                        "customerProductWeight": 0,
                        "date": "2022-01-30",
                        "discount": NULL,
                        "finalWeight": 107,
                        "grandTotalAmount": 196088,
                        "grandTotalWeight": 107,
                        "payedAmount": 196088,
                        "rate": rate.hallmarkRate,
                        "remainingAmount": 0,
                        "status": "submitted",
                        "totalAmount": 196088,
                        "advanceAmount": NULL,
                        "billProduct": [
                              {
                                    "billProductId": 1,
                                    "billId": 1,
                                    "lossWeight": 9,
                                    "makingCharge": 900,
                                    "quantity": 1,
                                    "rate": 90000,
                                    "totalAmountPerProduct": 196088,
                                    "totalWeight": NULL,
                                    "product":{
                                    "gemsName": "dimond",
                                    "gemsPrice": 98888,
                                    "netWeight": 98,
                                    "productId": 1,
                                    "productName": "Bala",
                                    "size": 0
                                    }
                              }
                        ]
                        }
                  ]
            }

            response = self.client.post('/api/bill/update', data,  format='json')
            self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue(response.data, 'Unable to update bill 1')
            

      #done
      def test_bill_for_orderedProduct(self):
            authenticate(self)

            data = {
                  "customerId": 1,
                  "email": "",
                  "name": "Kiraaan",
                  "phone": "9805169542",
                  "address": "nepal",
                  "bills": [
                        {
                              "orderId": 1,
                              "billId": NULL,
                              "advanceAmount": NULL,
                              "billType": "gold",
                              "customerProductAmount": 0,
                              "customerProductWeight": NULL,
                              "date": "2022-04-11",
                              "discount": NULL,
                              "finalWeight": 26,
                              "grandTotalAmount": 25780,
                              "grandTotalWeight": 26,
                              "payedAmount": NULL,
                              "rate": 98000,
                              "remainingAmount": 25780,
                              "status": "submitted",
                              "totalAmount": 25780,
                              "billProduct": [
                              {
                                    "lossWeight": "2",
                                    "makingCharge": "300",
                                    "quantity": 1,
                                    "rate": 98000,
                                    "totalAmountPerProduct": 25780,
                                    "totalWeight": 26,
                                    "product":{
                                          "productId": 1,
                                          "gemsName": "",
                                          "gemsPrice": NULL,
                                          "netWeight": 24,
                                          "productName": "earring",
                                          "size": NULL
                                    }
                              }
                        ]
                        }
                  ]
            }

            response = self.client.post('/api/generate-bill/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['name'], 'Kiraaan')
            self.assertTrue('bills' in response.data)
            self.assertTrue(response.data['bills'][0]['orderId'], 1)
            self.assertTrue('billProduct' in response.data['bills'][0])
            self.assertTrue('product' in response.data['bills'][0]['billProduct'][0])

      #done
      def test_bill_for_order_empty_field(self):
            authenticate(self)

            data = {
                  "customerId": 1,
                  "email": "",
                  "name": "",
                  "phone": "9805169542",
                  "address": "nepal",
                  "bills": [
                        {
                              "orderId": 1,
                              "billId": NULL,
                              "advanceAmount": NULL,
                              "billType": "gold",
                              "customerProductAmount": 0,
                              "customerProductWeight": NULL,
                              "date": "2022-04-11",
                              "discount": NULL,
                              "finalWeight": 26,
                              "grandTotalAmount": 25780,
                              "grandTotalWeight": 26,
                              "payedAmount": NULL,
                              "rate": 98000,
                              "remainingAmount": 25780,
                              "status": "submitted",
                              "totalAmount": 25780,
                              "billProduct": [],
                        } 
                  ]     
            }

            response = self.client.post('/api/generate-bill/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue(response.data['messsage'][0], 'BillProduct is missing')

      #done
      def test_bill_invalid(self):
            authenticate(self)

            data = {
                  "customerId": 1,
                  "email": 345345345,
                  "name": 324234234,
                  "phone": "9805169542",
                  "address": "nepal",
                  "bills": [
                        {
                              "orderId": 'dsfsdfsdf',
                              "billId": 'sdfsddsf',
                              "advanceAmount": NULL,
                              "billType": "gold",
                              "customerProductAmount": 0,
                              "customerProductWeight": NULL,
                              "date": "2022-04-11",
                              "discount": NULL,
                              "finalWeight": 26,
                              "grandTotalAmount": 25780,
                              "grandTotalWeight": 26,
                              "payedAmount": NULL,
                              "rate": 98000,
                              "remainingAmount": 25780,
                              "status": "submitted",
                              "totalAmount": 25780,
                              "billProduct": [],
                        } 
                  ]     
            }

            response = self.client.post('/api/generate-bill/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue(response.data['email'][0], "Enter a valid email address.")
            self.assertTrue(response.data['bills'][0]['orderId'][0], "Incorrect type Expected pk value, reveived str.")
            
            
      def test_sales_report(self):
            authenticate(self)

            response = self.client.get('/api/sales/report/?date=2022-04-01')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['labels'][0], "week1")

      def test_bill_product_monthly_report(self):
            authenticate(self)

            response = self.client.get('/api/bill-product/monthly/report/?date=2022-04-01')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
      
      def test_increment_report(self):
            authenticate(self)

            response = self.client.get('/api/bill-order-staffwork/increment/report/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue('bill' in response.data)
            self.assertTrue('total' in response.data['bill'])
            self.assertTrue('increment' in response.data['bill'])
            self.assertTrue('order' in response.data)
            self.assertTrue('total' in response.data['order'])
            self.assertTrue('increment' in response.data['order'])
            self.assertTrue('staffWork' in response.data)
            self.assertTrue('total' in response.data['staffWork'])
            self.assertTrue('increment' in response.data['staffWork'])
