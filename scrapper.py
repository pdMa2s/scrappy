import re
import requests

from bs4 import BeautifulSoup
from typing import List, Union


headers = {
    "USer-Agent": "Chrome/107.0.5304.68"
}

response = requests.get("https://www.digitec.ch/en/s1/product/apple-iphone-14-pro-256-gb-space-black-610-sim-esim-48-mpx-5g-mobile-phones-21997003", headers)
soup = BeautifulSoup(response.content, 'html.parser')

def get_product() -> str: 
    return soup.h1.strong.get_text() + soup.h1.span.get_text()

def parse_price(raw_price: str) -> Union[float, None]:
    return float(price_pattern_digits.group(0)) if (price_pattern_digits := re.search(r"\d+\.\d+", raw_price)) else \
    float(price_pattern_w_chars.group(0).split(".")[0]) if (price_pattern_w_chars := re.search(r"\d+\..", raw_price)) else None

def get_offers() -> List[float]:
    offers = []
    for offer_text in soup.find_all('strong'):
        if offer := parse_price(offer_text.get_text()):
            offers.append(offer)
    return offers

print(f"Product: {get_product()}\nOffers: {get_offers()}")
