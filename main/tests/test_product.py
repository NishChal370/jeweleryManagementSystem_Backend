from main.models import Product
from django.urls import reverse
from rest_framework import status
from asyncio.windows_events import NULL
from rest_framework.test import APITestCase
from main.tests.tests_auth import authenticate


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
            