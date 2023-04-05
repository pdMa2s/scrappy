import re
import requests

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import Optional

from storage import Product

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/41.0.2228.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'
           }


class Parser(ABC):
    @abstractmethod
    def get_product(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def get_price(self, soup: BeautifulSoup) -> Optional[float]:
        pass

    @abstractmethod
    def can_process_url(self, url: str) -> bool:
        pass

    def get_product_info(self, url: str) -> Product:
        assert self.can_process_url(url), f"{self.__str__()} can't process {url}"
        response = requests.get(url, headers=HEADERS)
        new_product = Product(url=url, name=None, current_price=None)
        if response.status_code not in (200, 201):
            return new_product
        try:
            soup = BeautifulSoup(response.content, features='lxml')
            new_product.name, new_product.current_price = self.get_product(soup), self.get_price(soup)
            return new_product
        except AttributeError:
            return new_product

    def __str__(self):
        return self.__class__.__name__


class ParserFactory:
    def __init__(self):
        self.parsers = {'Digitec': DigitecParser(), 'Amazon': AmazonParser(), 'Ottos': OttosParser()}

    def get_parser_with_url(self, url: str) -> Parser:
        for _, parser in self.parsers.items():
            if parser.can_process_url(url):
                return parser
        raise AttributeError(f"No parser for {url}")  # TODO: think of a better solution for this

    def get_parser_with_id(self, parser_id: str) -> Parser:
        assert parser_id in self.parsers
        return self.parsers[parser_id]


class DigitecParser(Parser):
    def can_process_url(self, url: str) -> bool:
        return re.search(r"https?://www\.digitec.+", url) is not None

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
    def can_process_url(self, url: str) -> bool:
        return re.search(r"https?://www\.amazon.+", url) is not None

    def get_product(self, soup: BeautifulSoup) -> str:
        return soup.find(id="productTitle").get_text().strip()

    def get_price(self, soup: BeautifulSoup) -> Union[float, None]:
        return float(soup.find(id='corePriceDisplay_desktop_feature_div')
                     .select('.a-offscreen')[0].get_text().replace('€', '').replace(',', '.'))


class OttosParser(Parser):
    def can_process_url(self, url: str) -> bool:
        return re.search(r"https?://www\.ottos.+", url) is not None

    def get_product(self, soup: BeautifulSoup) -> str:
        return soup.find("span", attrs={"data-ui-id": "page-title-wrapper"}).get_text()

    def get_price(self, soup: BeautifulSoup) -> Union[float, None]:
        return soup.find("span", attrs={"class": "price-wrapper"}).next_element.get_text().replace("CHF", "").strip()
