import re
import requests

from bs4 import BeautifulSoup
from discord import SyncWebhook
from typing import List, Union

webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1036384939878387723/pYZwx78HUlMxUv_6Br2kEsp69hQrxzzDqYz4UnWLn5qHs4hOptoF6IHLOswSqIKZ1h4T")

headers = {
    "USer-Agent": "Chrome/107.0.5304.68"
}
websites = {
    "Digitec" : [
        "https://www.digitec.ch/en/s1/product/xiaomi-mi-selfie-stick-tripod-mobile-phone-accessories-9868799"
        ],
    "Amazon": [
        "https://www.amazon.es/Profesional-Tupwoon-Resistente-Desmontable-Compatible/dp/B0B6BF9HT5",
        "https://www.amazon.es/Tr%C3%ADpode-Extensible-Inal%C3%A1mbrico-Control-Compatible/dp/B09KG9SMBV/"
        ]
}


class DigitecParser:
    def __init__(self, links: List[str]):
        self.links = links

    def get_product(self, soup) -> str: 
        return soup.h1.strong.get_text() + soup.h1.span.get_text()

    def parse_price(self, raw_price: str) -> Union[float, None]:
        return float(price_pattern_digits.group(0)) if (price_pattern_digits := re.search(r"\d+\.\d+", raw_price)) else \
        float(price_pattern_w_chars.group(0).split(".")[0]) if (price_pattern_w_chars := re.search(r"\d+\..", raw_price)) else None

    def get_price(self, soup) -> float:
        return self.parse_price(soup.find_all('strong')[0].get_text())

    def show_offers(self):
        for l in self.links:
            response = requests.get(l, headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            #print(f"Product: {self.get_product(soup)}\nPrice: {self.get_price(soup)}")
            webhook.send(f"Digitec:\n\t\t{self.get_product(soup)}\n\t\t - Link: {l}\n\t\t- Price: {self.get_price(soup)}")


        
class AmazonParser:
    def __init__(self, links: List[str]):
        self.links = links

    def get_product(self, soup) -> str: 
        return soup.find(id="productTitle").get_text().strip()

    def parse_price(self, raw_price: str) -> Union[float, None]:
        return float(raw_price)


    def get_price(self, soup) -> float:
        return float(soup.find(id='corePriceDisplay_desktop_feature_div').select('.a-offscreen')[0].get_text().replace('€', '').replace(',', '.'))

            
    def show_offers(self):
        for l in self.links:
            response = requests.get(l, headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            #print(f"Amazon:\n\t\t{self.get_product(soup)}\n\t\t- Link: {l}\n\t\t- Price: {self.get_price(soup)}")
            webhook.send(f"Amazon:\n\t\t{self.get_product(soup)}\n\t\t- Link: {l}\n\t\t- Price: {self.get_price(soup)}")

if __name__ == '__main__':
    digitec = DigitecParser(websites['Digitec'])
    digitec.show_offers()

    amazon = AmazonParser(websites["Amazon"])
    amazon.show_offers()