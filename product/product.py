from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    url: str
    name: Optional[str] = None
    last_price: Optional[str] = None
    min_price: Optional[str] = None
    min_price_date: Optional[datetime] = None
    max_price: Optional[str] = None
    max_price_date: Optional[datetime] = None

    def has_price(self) -> bool:
        return self.last_price is not None

    def has_name(self) -> bool:
        return self.name is not None
