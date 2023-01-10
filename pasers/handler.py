import asyncio
from typing import Union

import history
from offer import Offer
from notify import Broadcaster
from parsers import Parser, ParserFactory


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


class URLHandler:
    def __init__(self, broadcaster: Broadcaster, parser: Union[Parser, None] = None,
                 parser_factory: Union[ParserFactory, None] = None):
        assert parser or parser_factory

        self.broadcaster = broadcaster
        self.parser = parser
        self.parser_factory = parser_factory

    def handle(self, urls: list[str]):
        for url in urls:
            parser = self.parser_factory.get_parser_with_url(url) if self.parser_factory else self.parser
            assert parser.can_process_url(url)

            offer = parser.get_offer(url)
            history.store_price(offer.link, offer.price)
            if offer:
                last_price = history.get_price(url)
                if last_price and offer.price > last_price:
                    msg = get_price_increase_msg(parser, offer)
                elif last_price and offer.price < last_price:
                    msg = get_price_reduction_msg(parser, offer)
                else:
                    msg = get_price_msg(parser, offer)
            else:
                msg = get_failed_request_msg(parser, offer)

            asyncio.run(self.broadcaster.broadcast(msg))