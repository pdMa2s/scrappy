from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    url: str
    name: Optional[str] = None
    current_price: Optional[str] = None

    def has_price(self) -> bool:
        return self.current_price is not None
