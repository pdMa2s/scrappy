from dataclasses import dataclass


@dataclass
class Offer:
    link: str
    price: float
    product: str
