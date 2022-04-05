from django.urls import reverse
from main.models import Customer
from rest_framework import status
from rest_framework.test import APITestCase
from main.tests.tests_auth import authenticate



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