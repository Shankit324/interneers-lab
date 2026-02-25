# adapters/repository.py
from ..core.ports import ProductRepository
from ..core.domain import Product
from typing import Dict, List, Tuple

class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self._storage: Dict[int, Product] = {}
        self._counter = 1

    def save(self, product: Product) -> Product:
        if not product.id:
            product.id = self._counter
            self._counter += 1
        self._storage[product.id] = product
        return product

    def get_by_id(self, product_id: int):
        return self._storage.get(product_id)

    def get_all(self, limit: int, offset: int) -> Tuple[List[Product], int]:
        all_items = list(self._storage.values())
        return all_items[offset : offset + limit], len(all_items)
    
    def update(self, product: Product, product_id: int) -> Product:
        if product_id not in self._storage:
            return None
        self._storage[product_id] = product
        return product

    def delete(self, product_id: int) -> bool:
        if product_id in self._storage:
            del self._storage[product_id]
            return True
        return False
