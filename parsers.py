import re
import requests

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from offer import Offer
from typing import List, Union

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/41.0.2228.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'
           }


class Parser(ABC):
    links: list[str]
    offers: list[Offer]

    def __init__(self, links: List[str]):
        self.links = links

    @abstractmethod
    def get_product(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def get_price(self, soup: BeautifulSoup) -> Union[float, None]:
        pass

    def get_offers(self) -> list[Offer]:
        offers = []
        for link in self.links:
            try:
                response = requests.get(link, headers=HEADERS)
                soup = BeautifulSoup(response.content, features='lxml')
                if price := self.get_price(soup):
                    offers.append(Offer(link=link, product=self.get_product(soup), price=price))
            except AttributeError:
                offers.append(Offer(link=link, product=None, price=None))
        return offers

    def __str__(self):
        return self.__class__.__name__


class DigitecParser(Parser):
    def get_product(self, soup: BeautifulSoup) -> str:
        return soup.h1.strong.get_text() + soup.h1.span.get_text()

    @staticmethod
    def parse_price(raw_price: str) -> Union[float, None]:
        return float(price_pattern_digits.group(0)) if (price_pattern_digits := re.search(r"\d+\.\d+", raw_price)) else\
            float(price_pattern_w_chars.group(0).split(".")[0]) if (
                price_pattern_w_chars := re.search(r"\d+\..", raw_price)) else None

    def get_price(self, soup: BeautifulSoup) -> Union[float, None]:
        return self.parse_price(soup.find_all('strong')[0].get_text())


class AmazonParser(Parser):
    def get_product(self, soup: BeautifulSoup) -> str:
        return soup.find(id="productTitle").get_text().strip()

    def get_price(self, soup: BeautifulSoup) -> Union[float, None]:
        return float(soup.find(id='corePriceDisplay_desktop_feature_div')
                     .select('.a-offscreen')[0].get_text().replace('€', '').replace(',', '.'))


class OttosParser(Parser):
    def get_product(self, soup: BeautifulSoup) -> str:
        return soup.find("span", attrs={"data-ui-id": "page-title-wrapper"}).get_text()

    def get_price(self, soup: BeautifulSoup) -> Union[float, None]:
        return soup.find("span", attrs={"class": "price-wrapper"}).next_element.get_text().replace("CHF", "").strip()
