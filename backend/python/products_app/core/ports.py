# core/ports.py
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from .domain import Product

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