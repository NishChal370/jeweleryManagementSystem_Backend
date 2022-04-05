from datetime import date
from django.urls import reverse
from rest_framework import status
from asyncio.windows_events import NULL
from rest_framework.test import APITestCase
from main.models import Bill, BillProduct, Customer, Order, OrderProduct, Product, Rate, Staff, StaffWork, User
# Create your tests here.



def authenticate(self):  
      url = reverse('token_obtain_pair')
      user = User.objects.create_user(username='user', email='user@foo.com', password='abcd@12')
      user.is_active = False
      user.save()

      resp = self.client.post(url, {'email':'user@foo.com', 'password':'abcd@12'}, format='json')
      self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

      user.is_active = True
      user.save()

      resp = self.client.post(url, {'username':'user@foo.com', 'password':'abcd@12'}, format='json')
      self.assertEqual(resp.status_code, status.HTTP_200_OK)
      self.assertTrue('access' in resp.data)
      access_token = resp.data['access']

      self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {access_token}")


class TestRate(APITestCase):
      def setUp(self):
            Rate.objects.create(
                  hallmarkRate = 90000, 
                  tajabiRate = 89000, 
                  silverRate = 1600
            )

      def test_get_no_auth(self):
            response = self.client.get(reverse('rates-list'))

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

      def test_get_rates(self):
            authenticate(self)
            
            response = self.client.get(reverse('rates-list'))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, list)
            self.assertTrue('date' in response.data[0])
            self.assertTrue('tajabiRate' in response.data[0])
            self.assertTrue('silverRate' in response.data[0])
            self.assertTrue('hallmarkRate' in response.data[0])
      
      
      def test_set_rates(self):
            authenticate(self)

            data = {
                  'hallmarkRate': 98000, 
                  'tajabiRate': 96000, 
                  'silverRate': 17000
            }
            response = self.client.post(reverse('rate-set'), data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, dict)
            self.assertTrue('date' in response.data)
            self.assertTrue('tajabiRate' in response.data)
            self.assertTrue('silverRate' in response.data)
            self.assertTrue('hallmarkRate' in response.data)
            self.assertEqual(response.data['hallmarkRate'], 98000)

      
      def test_get_rate_by_date(self):
            authenticate(self)

            response = self.client.get('/api/rate/')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

            response = self.client.get('/api/rate/2022-04-05')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['date'], '2022-04-04')
            self.assertTrue('date' in response.data)
            self.assertTrue('tajabiRate' in response.data)
            self.assertTrue('silverRate' in response.data)
            self.assertTrue('hallmarkRate' in response.data)

      def test_get_rate_report(self):
            authenticate(self)

            response = self.client.get('/api/rate/report/?type=monthly')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, list)

            response = self.client.get('/api/rate/report/?type=weekly')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, list)

            response = self.client.get('/api/rate/report/?type=yearly')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, list)



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



class TestCustomer(APITestCase):
      def setUp(self):
            Customer.objects.create(
                  name = "Hari",
                  address = "nepal",
                  phone = "9805169542",
                  email = "np01cp4a190072@islingtoncollege.edu.np"
            )

      def test_get_customer_no_auth(self):
            response = self.client.get(reverse('customers-list'))

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

      def test_get_customer_list(self):
            authenticate(self)

            response = self.client.get(reverse('customers-list'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, dict)
      
      def test_get_custommer_by_id(self):
            authenticate(self)

            response = self.client.get('/api/customer/1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(1, response.data['customerId'])

      def test_customer_address_report(self): #address
            authenticate(self)

            response = self.client.get(reverse('customer-report'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, dict)


class TestProduct(APITestCase):
      def setUp(self):
            Product.objects.create(
                  productName = 'ring',
                  netWeight = 12,
                  size = NULL,
                  gemsName = 'muga',
                  gemsPrice = 1500,
            )

      def test_get_product_no_auth(self):
            response = self.client.get(reverse('product-list'))

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

      def test_get_products(self):
            authenticate(self)

            response = self.client.get(reverse('product-list'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, dict)
            

class TestStaff(APITestCase):
      def setUp(self):
            staff =  Staff.objects.create(
                  staffName = "ankit",
                  address = "Beni",
                  phone = "9878764857",
                  email = NULL,
                  registrationDate = "2022-02-15"
            )
            customer =  Customer.objects.create(
                  name = "Hari",
                  address = "nepal",
                  phone = "9805169542",
                  email = "np01cp4a190072@islingtoncollege.edu.np"
            )
            rate = Rate.objects.create(
                  hallmarkRate = 90000, 
                  tajabiRate = 89000, 
                  silverRate = 1600
            )
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
            StaffWork.objects.create(
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
      
      def test_get_Staff_detail(self):
            authenticate(self)

            response = self.client.get(reverse('staff-detail'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, dict)
      
      def test_get_staff_by_id(self):
            authenticate(self)

            response = self.client.get('/api/staff/1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(1, response.data['staffId'])

            response = self.client.get('/api/staff/2')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

      def test_update_staff_by_id(self):
            authenticate(self)

            data ={
                  "staffName": "Rohan",
                  "email": 'rohan123@gmail.com',
                  "address":'beni'
            }

            response = self.client.post('/api/staff-update/1', data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data[0]['address'],'beni')
            self.assertTrue(response.data[0]['staffName'],'Rohan')
            self.assertTrue(response.data[0]['email'],'rohan123@gmail.com')

      def test_register_staff(self):
            authenticate(self)

            data ={
                  "staffName": "rohan",
                  "address": "Baglung",
                  "phone": "9884768698",
                  "email": 'wetwerwerwerwerwe',
                  "registrationDate": "2022-02-15"
            }

            response = self.client.post(reverse('staff-register'),data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue(response.data['email'],'Enter a valid email address.')
            

            data ={
                  "staffName": "rohan",
                  "address": "Baglung",
                  "phone": "9884768698",
                  "email": 'rohan@gmail.com',
                  "registrationDate": "2022-02-15"
            }

            response = self.client.post(reverse('staff-register'),data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data ={
                  "phone": "9884768698",
                  "email": 'rohan@gmail.com',
                  "registrationDate": "2022-02-15"
            }

            response = self.client.post(reverse('staff-register'),data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue(response.data['address'][0],'This field is required')
            self.assertTrue(response.data['staffName'][0],'This field is required')
            
      def test_get_staff_name_list(self):
            authenticate(self)
            # get all staff name list
            response = self.client.get(reverse('staffs-name-list'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, list)
      
      def test_get_staff_work_detail(self):
            authenticate(self)

            # get all of page 1
            response = self.client.get('/api/staff/work/?submittionDate=&staffInfo=&orderId=&type=&workStatus=&page=1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, list)
            # search by staff name
            response = self.client.get('/api/staff/work/?submittionDate=&staffInfo=ankit&orderId=&type=&workStatus=&page=1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, list)
            self.assertEqual(response.data['results'][0]['staff']['staffName'], 'ankit')
            # search for report for today
            response = self.client.get('/api/staff/work/?submittionDate=&staffInfo=ankit&orderId=&type=&workStatus=&result=Today&page=1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, list)
            self.assertTrue(response.data['results'][0]['date'], date.today())

      def test_submit_staff_work(self):
            authenticate(self)
            data ={
                  'KDMWeight': 1,
                  "date": "2022-04-04",
                  "finalProductWeight": 13,
                  "givenWeight": 12,
                  "lossWeight": 0,
                  "orderProduct": 1,
                  "staff": 1,
                  "staffWorkId": 1,
                  "status": "inprogress",
                  "submittedDate": "2022-04-04",
                  "submittedWeight": 13,
                  "submittionDate": "2022-04-04",
                  "totalWeight": 13,
            }
            response = self.client.post(reverse('staff-work-assign'), data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, dict)
            self.assertTrue(response.data['submittionDate'], "2022-04-04")
            self.assertTrue(response.data['finalProductWeight'], 13)
                        

      def test_delete_staff_by_id(self):
            authenticate(self)

            response = self.client.delete('/api/staff/delete/1')
            self.assertEqual(response.status_code, status.HTTP_428_PRECONDITION_REQUIRED)
            self.assertTrue(response.data, 'ankit have work to complete')



class TestAdmin(APITestCase):
      def setUp(self):
            User.objects.create(
                  full_name = "Nirmal",
                  pan_number = 1238497675,
                  phone = 98576300654,
                  profileImage = 'image.jpg',
                  register_date = date.today(),
                  email = 'nirmal@gmail.com',
            )

      def test_get_admin(self):
            authenticate(self)

            response = self.client.get(reverse('admin-detail'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['full_name'], 'Nirmal')
            self.assertTrue(response.data['register_date'], date.today())
      
      def test_update_admin(self):
            authenticate(self)

            data={
                  'username' :'Nirmal',
                  'full_name' : "Nirmal Bishwokarma",
                  'pan_number' : 1238497675,
                  'phone' : 9876765643,
                  'email': 'nirmal@gmail.com'
            }
            response = self.client.post(reverse('admin-detail-update'), data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['full_name'], 'Nirmal Bishwokarma')
            self.assertTrue(response.data['phone'], 9876765643)

            data={
                  'username' :'Nirmal',
                  'phone' : '-9876',
            }
            response = self.client.post(reverse('admin-detail-update'), data)
            self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue(response.data, 'invalid phone data type')


      def test_change_password(self):
            authenticate(self)

            data={}
            response = self.client.patch(reverse('change-password'), data)
            self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue(response.data['old_password'], 'The field is required.')
            self.assertTrue(response.data['new_password'], 'The field is required.')

            data={
                  'old_password': 'nothing@#12',
                  'new_password': 'nothing@12',
                  'new_password2': 'nothing@12',
            }
            response = self.client.patch(reverse('change-password'), data)
            self.assertTrue(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, {'password changed'})

      def test_Reset_password_by_token(self):
            authenticate(self)
            data={
                  'email':'nirmal@gmail.com'
            }
            response = self.client.post('/api/password_reset/', data)
            self.assertTrue(response.status_code, status.HTTP_200_OK)



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

      def test_delete_order_by_id(self):
            authenticate(self)

            response = self.client.delete('/api/order-delete/1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data, {'Order 1 is deleted'})       

      def test_get_order_summmary(self):
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
      

class TestLogout(APITestCase):
      def setUp(self):
            User.objects.create(
                  full_name = "Nirmal",
                  pan_number = 1238497675,
                  phone = 98576300654,
                  profileImage = 'image.jpg',
                  register_date = date.today(),
                  password = 'nothing@#12',
                  email = 'nirmal@gmail.com',
            )

      def test_logout(self):
            authenticate(self)

            response = self.client.post('/api/logout/')
            self.assertTrue(response.status_code, status.HTTP_200_OK)
