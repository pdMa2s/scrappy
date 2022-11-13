import json

from typing import Union

PRICE_FILE_NAME = "price_history.json"
PRICE_FILE = open("price_history.json", "r")
PRICES = json.load(PRICE_FILE)
PRICE_FILE.close()


def get_price(link: str) -> Union[float, None]:
    return PRICES[link] if link in PRICES else None


def store_price(link: str, price: float):
    PRICES[link] = price


def commit():
    with open(PRICE_FILE_NAME, "w") as price_file:
        json.dump(PRICES, price_file)


if __name__ == '__main__':
    print(PRICE_FILE)
