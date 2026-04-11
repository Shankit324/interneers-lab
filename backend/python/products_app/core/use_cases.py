# core/use_cases.py
from .ports import ProductRepository, CategoryRepository
from .domain import Product, ProductCategory
import csv
import io


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create_product(self, data: dict) -> Product:
        # Basic Validation
        if data.get('price', 0) <= 0:
            raise ValueError("Price must be positive")
            
        # Mapping 'category' from JSON to 'category_id' for the Domain
        category_id = data.get('category') or data.get('category_id')
        
        # Create domain object with explicit arguments to avoid TypeError
        product = Product(
            name=data.get('name'),
            price=float(data.get('price')),
            brand=data.get('brand'),
            category_id=category_id,
            description=data.get('description', ""),
            quantity=data.get('quantity', 0)
        )
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
    
    def bulk_create_from_csv(self, csv_file_content: str):
        """Requirement 6: Bulk POST via CSV"""
        f = io.StringIO(csv_file_content)
        reader = csv.DictReader(f)
        products = []
        for row in reader:
            # Requirement 5: Handling existing/missing brands with a default
            brand = row.get('brand') or "Legacy Brand"
            product = Product(
                name=row['name'],
                price=float(row['price']),
                brand=brand,
                category_id=row.get('category_id'),
                description=row.get('description', "")
            )
            products.append(product)
        self.repo.bulk_save(products)

    def filter_products(self, category_ids: list[str]):
        """Advanced 2: Rich Filters"""
        return self.repo.get_by_filters(category_ids=category_ids)
        
class ProductCategoryService:
    def __init__(self, category_repo: CategoryRepository, product_repo: ProductRepository):
        self.category_repo = category_repo
        self.product_repo = product_repo

    def create_category(self, title: str, description: str) -> ProductCategory:
        category = ProductCategory(title=title, description=description)
        return self.category_repo.save(category)

    def list_products_in_category(self, category_id: str) -> list[Product]:
        return self.product_repo.get_by_category(category_id)

    def assign_product_to_category(self, product_id: str, category_id: str):
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise LookupError("Product not found")
        product.category_id = category_id
        return self.product_repo.save(product)

    def remove_product_from_category(self, product_id: str):
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise LookupError("Product not found")
        product.category_id = None
        return self.product_repo.save(product)
    
    def list_all_categories(self) -> List[ProductCategory]:
        """Fetches all categories from the repository"""
        return self.category_repo.get_all()
    
    def get_products_in_category(self, category_id: str) -> List[Product]:
        """Requirement 3a: Fetches products belonging to a specific category."""
        return self.product_repo.get_by_category(category_id)