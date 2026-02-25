# core/use_cases.py
from .ports import ProductRepository
from .domain import Product

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create_product(self, data: dict) -> Product:
        # Basic Validation
        if data['price'] <= 0:
            raise ValueError("Price must be positive")
        if data['quantity'] < 0:
            raise ValueError("Quantity cannot be negative")
            
        product = Product(**data)
        return self.repo.save(product)
    
    def get_product(self, product_id) -> Product:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise LookupError(f"Product {product_id} not found")
        return product

    def list_products(self, page: int = 1, size: int = 10):
        offset = (page - 1) * size
        return self.repo.get_all(limit=size, offset=offset)
    
    def update_product(self, product_id, data: dict) -> Product:
        product = self.repo.update(data, product_id)
        if not product:
            raise LookupError(f"Product {product_id} not found")
        return product

    def delete_product(self, product_id: int):
        success = self.repo.delete(product_id)
        if not success:
            raise LookupError(f"Product {product_id} not found")