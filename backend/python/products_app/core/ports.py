# core/ports.py
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from .domain import Product, ProductCategory

class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: ProductCategory) -> ProductCategory: pass

    @abstractmethod
    def get_by_id(self, category_id: str) -> Optional[ProductCategory]: pass

    @abstractmethod
    def get_all(self) -> List[ProductCategory]: pass

    @abstractmethod
    def delete(self, category_id: str) -> bool: pass

class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> Product: pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]: pass

    @abstractmethod
    def get_all(self, limit: int, offset: int) -> Tuple[List[Product], int]: pass

    @abstractmethod
    def update(self, data: Product, product_id: int) -> Product: pass

    @abstractmethod
    def delete(self, product_id: int) -> bool: pass

    @abstractmethod
    def get_by_category(self, category_id: str) -> List[Product]: pass

    @abstractmethod
    def get_by_filters(self, category_ids: List[str], min_price: Optional[float] = None) -> List[Product]: pass

    @abstractmethod
    def bulk_save(self, products: List[Product]) -> None: pass