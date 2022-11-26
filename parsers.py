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
    @abstractmethod
    def get_product(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def get_price(self, soup: BeautifulSoup) -> Union[float, None]:
        pass

    @abstractmethod
    def can_process_url(self, url: str) -> bool:
        pass

    def get_offer(self, url) -> Offer:
        assert self.can_process_url(url), f"{self.__str__()} can't process {url}"
        try:
            response = requests.get(url, headers=HEADERS)
            if response.status_code not in (200, 201):
                return Offer(link=url, product=None, price=None)

            soup = BeautifulSoup(response.content, features='lxml')
            price = self.get_price(soup)
            return Offer(link=url, product=self.get_product(soup), price=price)
        except AttributeError or AssertionError:
            return Offer(link=url, product=None, price=None)

    def __str__(self):
        return self.__class__.__name__


class ParserHandler:
    parsers: list[Parser]

    def __init__(self, parsers):
        self.parsers = parsers

    def get_parser(self, url: str):
        for parser in self.parsers:
            if parser.can_process_url(url):
                return parser
        raise AttributeError(f"No parser for {url}")  # TODO: think of a better solution for this


class ParserFactory:
    @staticmethod
    def get_parser(parser_id: str) -> Parser:
        if parser_id == 'Amazon':
            return AmazonParser()
        elif parser_id == 'Digitec':
            return DigitecParser()
        elif parser_id == 'Ottos':
            return OttosParser()
        else:
            raise AttributeError("Invalid parser")


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
