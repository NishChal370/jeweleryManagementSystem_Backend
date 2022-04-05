from datetime import date
from main.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


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
