from datetime import date
from django.urls import reverse
from rest_framework import status
from asyncio.windows_events import NULL
from rest_framework.test import APITestCase
from main.tests.tests_auth import authenticate
from main.models import Customer, Order, OrderProduct, Product, Rate, Staff, StaffWork

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