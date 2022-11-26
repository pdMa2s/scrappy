from dataclasses import dataclass
from typing import Union


@dataclass
class Offer:
    link: str
    price: Union[float, None]
    product: Union[str, None]

    def __bool__(self):
        return self.price is not None
