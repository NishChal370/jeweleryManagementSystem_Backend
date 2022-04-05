from datetime import date
from django.urls import reverse
from rest_framework import status
from asyncio.windows_events import NULL
from rest_framework.test import APITestCase
from main.tests.tests_auth import authenticate
from main.models import Bill, BillProduct, Customer, Product, Rate



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
            
            response = self.client.delete('/api/bill/delete/1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response = self.client.delete('/api/bill/delete/1')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertTrue(response.data['message'], 'Not Found !!')

      def test_get_bills_summary(self):
            authenticate(self)

            response = self.client.get(reverse('bill-list-summmary'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

      def test_bill_summary_filter(self): #=
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
            self.assertEqual([], response.data['results'])

           
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
                        # 'orderId': NULL,
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
            self.assertTrue(response.data['name'], 'Kiraaan')
            self.assertTrue(response.data['address'], 'America')

            
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
