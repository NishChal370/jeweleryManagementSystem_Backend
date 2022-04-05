from datetime import date
from main.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from main.tests.tests_auth import authenticate



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
