# products_app/tests/test_use_cases.py
import unittest
from products_app.core.use_cases import ProductService
from products_app.adapters.repository import InMemoryProductRepository

class TestProductService(unittest.TestCase):
    def setUp(self):
        # This runs before every single test, giving us a fresh, empty repository
        self.repo = InMemoryProductRepository()
        self.service = ProductService(self.repo)
        
        self.valid_data = {
            "name": "Test Laptop",
            "description": "A fast laptop",
            "category": "Electronics",
            "price": 999.99,
            "brand": "TechCorp",
            "quantity": 10
        }

    def test_create_product_success(self):
        # Act
        product = self.service.create_product(self.valid_data)
        
        # Assert
        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, "Test Laptop")
        self.assertEqual(self.repo._counter, 2) # Proves it was saved

    def test_create_product_negative_price_fails(self):
        # Arrange
        bad_data = self.valid_data.copy()
        bad_data['price'] = -50.00
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.service.create_product(bad_data)
            
        self.assertTrue("Price must be positive" in str(context.exception))