# products_app/tests/test_integration.py
from rest_framework.test import APITestCase
from mongoengine import connect, disconnect
from products_app.models import ProductCategoryDocument, ProductDocument

class TestProductAPIIntegration(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Disconnect from default and connect to a dedicated test database
        disconnect(alias='default')
        connect('test_db', host='mongodb://localhost:27017/test_db', alias='default')

    def setUp(self):
        # Seed a category document directly into the test database before each test
        self.cat = ProductCategoryDocument(title="Kitchen", description="Essentials").save()

    def tearDown(self):
        # Clean up the collections after each test to ensure a clean slate
        ProductCategoryDocument.objects.delete()
        ProductDocument.objects.delete()

    @classmethod
    def tearDownClass(cls):
        # Disconnect when all tests in this class are done
        disconnect(alias='default')
        super().tearDownClass()

    def test_create_product_api(self):
        """Tests POST /api/products/"""
        payload = {
            "name": "Cast Iron Pan", 
            "price": 25.0, 
            "brand": "Lodge", 
            "category": str(self.cat.id),
            "quantity": 5
        }
        
        response = self.client.post('/api/products/', payload, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "Cast Iron Pan")
        
        # Verify it actually saved in the DB
        self.assertEqual(ProductDocument.objects.count(), 1)

    def test_bulk_upload_api(self):
        """Tests POST /api/products/bulk-upload/"""
        import io
        
        # Create an in-memory CSV file string
        csv_content = f"name,price,brand,category_id\nMilk,4.0,Farm,{str(self.cat.id)}\nEggs,3.0,Farm,{str(self.cat.id)}"
        
        # Convert it to a file-like object for the test client
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = 'test_upload.csv'
        
        response = self.client.post('/api/products/bulk-upload/', {'file': file}, format='multipart')
        
        self.assertEqual(response.status_code, 201)
        # Verify both products were saved to the test DB
        self.assertEqual(ProductDocument.objects.count(), 2)

    def test_list_categories_api(self):
        """Tests GET /api/categories/"""
        response = self.client.get('/api/categories/')
        
        self.assertEqual(response.status_code, 200)
        # Should return 1 because we seeded 1 in setUp()
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Kitchen")