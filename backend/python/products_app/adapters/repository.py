# products_app/adapters/repository.py
from typing import List, Optional, Tuple
from mongoengine.errors import DoesNotExist
from ..core.ports import ProductRepository, CategoryRepository
from ..core.domain import Product as DomainProduct, ProductCategory as DomainCategory
from products_app.models import ProductDocument, ProductCategoryDocument

class MongoProductRepository(ProductRepository):
    
    def _to_domain(self, doc: ProductDocument) -> DomainProduct:
        """Helper to convert Mongo Document to Domain Dataclass with safe dereferencing"""
        category_id = None
        try:
            # Safe dereferencing: wrap in try-except to prevent DoesNotExist crash
            if doc.category:
                category_id = str(doc.category.id)
        except DoesNotExist:
            category_id = None

        return DomainProduct(
            id=str(doc.id),
            name=doc.name,
            description=doc.description,
            category_id=category_id, # Maps to domain 'category_id'
            price=doc.price,
            brand=doc.brand, # Requirement 5: Required brand
            quantity=doc.quantity,
            created_at=doc.created_at,
            updated_at=doc.updated_at
        )

    def save(self, product: DomainProduct) -> DomainProduct:
        """Requirement 3: CRUD - Create"""
        doc = ProductDocument(
            name=product.name,
            brand=product.brand,
            category=product.category_id,
            price=product.price,
            description=product.description,
            quantity=product.quantity
        ).save()
        return self._to_domain(doc)

    def update(self, data: DomainProduct, product_id: str) -> DomainProduct:
        """Requirement 3: CRUD - Update (Fixes TypeError and dict access)"""
        doc = ProductDocument.objects(id=product_id).first()
        if not doc:
            raise LookupError(f"Product {product_id} not found")
        
        # Access attributes directly from the dataclass, not as a dict
        doc.name = data.name
        doc.description = data.description
        doc.category = data.category_id
        doc.price = data.price
        doc.brand = data.brand
        doc.quantity = data.quantity
        doc.save()
        
        return self._to_domain(doc)

    def get_by_id(self, product_id: str) -> Optional[DomainProduct]:
        doc = ProductDocument.objects(id=product_id).first()
        return self._to_domain(doc) if doc else None

    def get_all(self, limit: int, offset: int) -> Tuple[List[DomainProduct], int]:
        query = ProductDocument.objects.skip(offset).limit(limit)
        total = ProductDocument.objects.count()
        return [self._to_domain(doc) for doc in query], total

    def delete(self, product_id: str) -> bool:
        doc = ProductDocument.objects(id=product_id).first()
        if doc:
            doc.delete()
            return True
        return False
    
    def get_by_category(self, category_id: str) -> List[DomainProduct]:
        """Requirement 3a: Fetch products belonging to a particular category"""
        docs = ProductDocument.objects(category=category_id)
        return [self._to_domain(doc) for doc in docs]

    def get_by_filters(self, category_ids: List[str]) -> List[DomainProduct]:
        """Advanced 2: Fetch products using a list of categories"""
        docs = ProductDocument.objects(category__in=category_ids)
        return [self._to_domain(doc) for doc in docs]

    def bulk_save(self, products: List[DomainProduct]) -> None:
        """Requirement 6: Bulk create products"""
        docs = [
            ProductDocument(
                name=p.name, price=p.price, brand=p.brand, 
                category=p.category_id, description=p.description, quantity=p.quantity
            ) for p in products
        ]
        ProductDocument.objects.insert(docs)

    # Inside MongoProductRepository in adapters/repository.py
    def delete(self, product_id: str) -> bool:
        """Requirement 3: CRUD - Delete Product"""
        # Locate the product document using the provided ID string
        doc = ProductDocument.objects(id=product_id).first()
        if doc:
            # Delete the product record
            doc.delete()
            return True
        return False

class MongoCategoryRepository(CategoryRepository):
    
    def _to_domain(self, doc: ProductCategoryDocument) -> DomainCategory:
        """Requirement 1: Category Domain mapping (No 'category' attribute check)"""
        return DomainCategory(
            id=str(doc.id),
            title=doc.title,
            description=doc.description,
            created_at=doc.created_at,
            updated_at=doc.updated_at
        )

    def save(self, category: DomainCategory) -> DomainCategory:
        """Requirement 3: CRUD - Category"""
        if category.id:
            ProductCategoryDocument.objects(id=category.id).update(
                title=category.title, description=category.description
            )
            doc = ProductCategoryDocument.objects(id=category.id).first()
        else:
            doc = ProductCategoryDocument(
                title=category.title, description=category.description
            ).save()
        return self._to_domain(doc)

    def get_by_id(self, category_id: str) -> Optional[DomainCategory]:
        doc = ProductCategoryDocument.objects(id=category_id).first()
        return self._to_domain(doc) if doc else None

    def get_all(self) -> List[DomainCategory]:
        """Requirement Advanced 1: Verification of seeded categories"""
        docs = ProductCategoryDocument.objects.all()
        return [self._to_domain(doc) for doc in docs]
    
    # Inside MongoCategoryRepository in adapters/repository.py
    def delete(self, category_id: str) -> bool:
        """Requirement 3: CRUD - Delete Category"""
        # Attempt to find the category document by its unique ID
        doc = ProductCategoryDocument.objects(id=category_id).first() 
        if doc:
            # Perform the deletion from MongoDB
            doc.delete() 
            return True
        return False # Return False if the ID does not exist