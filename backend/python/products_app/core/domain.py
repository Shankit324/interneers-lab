# products_app/core/domain.py
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class ProductCategory:
    title: str
    description: str
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Product:
    name: str
    price: float
    brand: str  # strictly required 
    category_id: Optional[str] = None # Linking to the Category ID
    description: str = ""
    quantity: int = 0
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None