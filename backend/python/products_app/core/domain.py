# products_app/core/domain.py
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class Product:
    name: str
    description: str
    category: str
    price: float
    brand: str
    quantity: int
    id: Optional[str] = None  # Changed to str for MongoDB ObjectId
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None