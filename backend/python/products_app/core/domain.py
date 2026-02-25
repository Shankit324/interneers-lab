# core/domain.py
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Product:
    name: str
    description: str
    category: str
    price: float
    brand: str
    quantity: int
    id: Optional[int] = None