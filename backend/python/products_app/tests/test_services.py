# products_app/tests/test_services.py
import unittest
from unittest.mock import MagicMock
from ..core.use_cases import ProductService, ProductCategoryService
from ..core.domain import Product, ProductCategory

class TestProductService(unittest.TestCase):
    def setUp(self):
        # Create a mock repository to pass into the service
        self.mock_repo = MagicMock()
        self.service = ProductService(self.mock_repo)

    def test_create_product_success(self):
        # Setup mock data (using the correct 'category_id' key)
        data = {
            "name": "Test Milk", 
            "price": 4.5, 
            "brand": "TestBrand", 
            "category_id": "66170d1234567890abcdef12",
            "quantity": 10
        }
        
        # Tell the mock repo what to return when .save() is called
        self.mock_repo.save.return_value = Product(**data, id="mock_id_123")

        # Execute the service method
        result = self.service.create_product(data)

        # Verify the repository was called and the result is correct
        self.mock_repo.save.assert_called_once()
        self.assertEqual(result.name, "Test Milk")
        self.assertEqual(result.brand, "TestBrand")

class TestCategoryService(unittest.TestCase):
    def setUp(self):
        self.mock_cat_repo = MagicMock()
        self.mock_prod_repo = MagicMock()
        self.service = ProductCategoryService(self.mock_cat_repo, self.mock_prod_repo)

    def test_list_all_categories(self):
        # Setup the mock to return a list containing one category
        mock_category = ProductCategory(title="Food", description="test description", id="cat_123")
        self.mock_cat_repo.get_all.return_value = [mock_category]
        
        # Execute the service method
        categories = self.service.list_all_categories()
        
        # Verify the results
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0].title, "Food")
        self.mock_cat_repo.get_all.assert_called_once()

    def test_get_products_in_category(self):
        # Setup
        self.mock_prod_repo.get_by_category.return_value = []
        
        # Execute
        self.service.get_products_in_category("cat_123")
        
        # Verify
        self.mock_prod_repo.get_by_category.assert_called_once_with("cat_123")