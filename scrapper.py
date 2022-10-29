import re
import requests

from bs4 import BeautifulSoup
from typing import List, Union


headers = {
    "USer-Agent": "Chrome/107.0.5304.68"
}

response = requests.get("https://www.digitec.ch/en/s1/product/noctua-nh-d15-chromax-165-mm-cpu-coolers-12111628", headers)
soup = BeautifulSoup(response.content, 'html.parser')

def get_product() -> str: 
    return soup.h1.strong.get_text() + soup.h1.span.get_text()

def parse_price(raw_price: str) -> Union[float, None]:
    return float(price_pattern.group(0)) if (price_pattern := re.search(r"\d+\.(\d+|.)", raw_price)) else None

def get_offers() -> List[float]:
    offers = []
    for offer_text in soup.find_all('strong'):
        if offer := parse_price(offer_text.get_text()):
            offers.append(offer)
    return offers

print(f"Product: {get_product()}\nPrice: {get_offers()}")
