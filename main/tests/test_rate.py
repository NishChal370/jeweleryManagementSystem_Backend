from main.models import Rate
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from main.tests.tests_auth import authenticate



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

