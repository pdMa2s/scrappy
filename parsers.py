from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from offer import Offer
from typing import List

class Parser(ABC):
    links: list[str]
    offers: list[Offer]

    def __init__(self, links: List[str]):
        self.links = links
        
    @abstractmethod
    def get_offers(self) -> list[Offer]:
        pass