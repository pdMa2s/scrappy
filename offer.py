from dataclasses import dataclass
from typing import Union


@dataclass
class Offer:
    link: str
    price: Union[float, None]
    product: Union[str, None]
