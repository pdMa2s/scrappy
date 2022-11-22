import argparse
import json
from discord import SyncWebhook

import history
from offer import Offer
from parsers import AmazonParser, DigitecParser, OttosParser, Parser


def parse_args():
    arg_parser = argparse.ArgumentParser(
        prog='Scrapy',
        description='Scrapes the provided urls for products and price quotes.',
        epilog='Text at the bottom of help'
    )

    cmd_line_group = arg_parser.add_argument_group('Command line group')
    cmd_line_group.add_argument('urls', action='append')
    cmd_line_group.add_argument('-p', '--parser', required=False, type=str)

    file_group = arg_parser.add_argument_group('File group')
    file_group.add_argument('-um', '--urls-map', type=argparse.FileType('r'))


webhook = SyncWebhook.from_url(
    "https://discord.com/api/webhooks/1041809526220927007/"
    "l2kSrqXnI1CP17I8DEA_s52H1Dwr_OZnP2JIZzk7dHk3BOPqdISW-GxhyY3Op0sBU97C"
)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/41.0.2228.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'
           }
websites = {
    "Digitec": [
        "https://www.digitec.ch/en/s1/product/xiaomi-mi-selfie-stick-tripod-mobile-phone-accessories-9868799"
    ],
    "Amazon": [
        "https://www.amazon.es/Profesional-Tupwoon-Resistente-Desmontable-Compatible/dp/B0B6BF9HT5",
        "https://www.amazon.es/Tr%C3%ADpode-Extensible-Inal%C3%A1mbrico-Control-Compatible/dp/B09KG9SMBV/"
    ],
    "Ottos": [
        "https://www.ottos.ch/de/electrolux-beutelloser-staubsauger-ease-c4-ec412sw-235108.html"
    ]
}


def get_failed_request_msg(parser: Parser, offer: Offer) -> str:
    return f"Failed request to {parser.__str__()[:-6]} try to fetch the link: {offer.link}"


def get_price_reduction_msg(parser: Parser, offer: Offer) -> str:
    return f"{parser.__str__()[:-6]}:  ----- Price reduction!!! ----\n\t\t{offer.product}" \
           f"\n\t\t- Link: {offer.link}\n\t\t- Price: {offer.price}"


def get_price_increase_msg(parser: Parser, offer: Offer) -> str:
    return f"{parser.__str__()[:-6]}:  ----- Price increase!!! ----\n\t\t{offer.product}" \
           f"\n\t\t- Link: {offer.link}\n\t\t- Price: {offer.price}"


def get_price_msg(parser: Parser, offer: Offer) -> str:
    return f"{parser.__str__()[:-6]}:\n\t\t{offer.product}\n\t\t- Link: {o.link}\n\t\t- Price: {o.price}"


if __name__ == '__main__':
    parsers = [DigitecParser(), AmazonParser(), OttosParser()]
    for p in parsers:
        for o in p.get_offer():
            last_price = history.get_price(o.link)
            if o.price:
                if last_price and last_price < o.price:
                    msg = get_price_reduction_msg(p, o)
                elif last_price and last_price > o.price:
                    msg = get_price_increase_msg(p, o)
                else:
                    msg = get_price_msg(p, o)
                history.store_price(o.link, o.price)
            else:
                msg = get_failed_request_msg(p, o)

            print(msg)
            webhook.send(msg)
    history.commit()
