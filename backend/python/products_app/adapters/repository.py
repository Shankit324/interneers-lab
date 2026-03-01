# products_app/adapters/repository.py
from typing import List, Optional, Tuple
from ..core.ports import ProductRepository
from ..core.domain import Product as DomainProduct
from products_app.models import ProductDocument

class MongoProductRepository(ProductRepository):
    
    def _to_domain(self, doc: ProductDocument) -> DomainProduct:
        """Helper to convert Mongo Document to Domain Dataclass"""
        return DomainProduct(
            id=str(doc.id),
            name=doc.name,
            description=doc.description,
            category=doc.category,
            price=doc.price,
            brand=doc.brand, 
            quantity=doc.quantity,
            created_at=doc.created_at,
            updated_at=doc.updated_at
        )

    def save(self, product: DomainProduct) -> DomainProduct:
        if product.id:
            # Update existing
            doc = ProductDocument.objects(id=product.id).first()
            if doc:
                doc.name = product.name
                doc.description = product.description
                doc.category = product.category
                doc.price = product.price
                doc.brand = product.brand
                doc.quantity = product.quantity
                doc.save()
            else:
                raise LookupError("Product not found")
        else:
            # Create new
            doc = ProductDocument(
                name=product.name,
                description=product.description,
                category=product.category,
                price=product.price,
                brand=product.brand,
                quantity=product.quantity
            )
            doc.save()
            
        return self._to_domain(doc)

    def get_by_id(self, product_id: str) -> Optional[DomainProduct]:
        doc = ProductDocument.objects(id=product_id).first()
        if doc:
            return self._to_domain(doc)
        return None

    def get_all(self, limit: int, offset: int) -> Tuple[List[DomainProduct], int]:
        query = ProductDocument.objects.skip(offset).limit(limit)
        total = ProductDocument.objects.count()
        return [self._to_domain(doc) for doc in query], total

    def update(self, data: DomainProduct, product_id: str) -> DomainProduct:
        doc = ProductDocument.objects(id=product_id).first()
        if not doc:
            raise LookupError(f"Product {product_id} not found")
        
        doc.name = data['name']
        doc.description = data['description']
        doc.category = data['category']
        doc.price = data['price']
        doc.brand = data['brand']
        doc.quantity = data['quantity']
        doc.save()
        
        return self._to_domain(doc)
        
    def delete(self, product_id: str) -> bool:
        doc = ProductDocument.objects(id=product_id).first()
        if doc:
            doc.delete()
            return True
        return False