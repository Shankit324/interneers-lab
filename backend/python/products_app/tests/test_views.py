# products_app/tests/test_views.py
from django.test import SimpleTestCase
from rest_framework.test import APIClient
from rest_framework import status

# Import our global storage so we can reset it!
from products_app.adapters.views import storage 

class ProductAPITests(SimpleTestCase):
    def setUp(self):
        storage._storage.clear()
        storage._counter = 1

        self.client = APIClient()
        self.url = '/api/products/' 
        self.valid_payload = {
            "name": "API Mouse",
            "description": "Click click",
            "category": "Peripherals",
            "price": 25.00,
            "brand": "Logi",
            "quantity": 100
        }

    def test_create_product_via_api(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "API Mouse")
        self.assertIn('id', response.data)

    def test_get_product_list(self):
        # Arrange: Create a product first
        self.client.post(self.url, self.valid_payload, format='json')
        
        # Act
        response = self.client.get(self.url)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Now this will correctly equal 1!
        self.assertEqual(len(response.data['items']), 1)