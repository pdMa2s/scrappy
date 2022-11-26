import argparse
import json
from argparse import Action, Namespace
from discord import SyncWebhook
from typing import Union

import history
from offer import Offer
from parsers import AmazonParser, DigitecParser, OttosParser, Parser, ParserFactory


def parse_args() -> Namespace:
    class JsonArgumentLoaderAction(Action):
        def __call__(self, *args, **kwargs):
            with open(args[2], 'r') as url_file:
                values = json.load(url_file)
                setattr(args[1], self.dest, values)

    arg_parser = argparse.ArgumentParser(
        prog='Scrapy',
        description='Scrapes the provided urls for products and price quotes.',
        epilog='Text at the bottom of help'
    )

    exclusive_group = arg_parser.add_mutually_exclusive_group()
    exclusive_group.add_argument('-u', '--urls', action='extend', nargs='+')
    exclusive_group.add_argument('-uf', '--urls-file', action=JsonArgumentLoaderAction)
    arg_parser.add_argument('-p', '--parser', required=False, type=str)

    parsed_args = arg_parser.parse_args()

    assert parsed_args.urls or parsed_args.urls_file
    return parsed_args


webhook = SyncWebhook.from_url(
    "https://discord.com/api/webhooks/1041809526220927007/"
    "l2kSrqXnI1CP17I8DEA_s52H1Dwr_OZnP2JIZzk7dHk3BOPqdISW-GxhyY3Op0sBU97C"
)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/41.0.2228.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'
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
    return f"{parser.__str__()[:-6]}:\n\t\t{offer.product}\n\t\t- Link: {offer.link}\n\t\t- Price: {offer.price}"


if __name__ == '__main__':
    user_args = parse_args()
    parsers = [DigitecParser(), AmazonParser(), OttosParser()]

    if user_args.urls_file:
        parser_links = user_args.urls_file
        for parser_name in parser_links:
            parser = ParserFactory.get_parser(parser_name)
            for url in parser_links[parser_name]:
                assert parser.can_process_url(url)

                if offer := parser.get_offer(url):
                    last_price = history.get_price(url)
                    if last_price and last_price < offer.price:
                        msg = get_price_reduction_msg(parser, offer)
                    elif last_price and last_price > offer.price:
                        msg = get_price_increase_msg(parser, offer)
                    else:
                        msg = get_price_msg(parser, offer)
                    history.store_price(offer.link, offer.price)
                else:
                    msg = get_failed_request_msg(parser, offer)

                print(msg)
                webhook.send(msg)
        history.commit()
