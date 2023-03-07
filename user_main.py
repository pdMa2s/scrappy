import argparse
import json
from argparse import Action, Namespace
from typing import Union

import history
from notify import Broadcaster, DiscordNotifier, StandardOutputNotifier
from pasers.offer import Offer
from pasers.parsers import Parser, ParserFactory


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
    arg_parser.add_argument('-b', '--bot', required=False)

    parsed_args = arg_parser.parse_args()

    assert parsed_args.urls or parsed_args.urls_file
    return parsed_args


DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1041809526220927007/" \
                  "l2kSrqXnI1CP17I8DEA_s52H1Dwr_OZnP2JIZzk7dHk3BOPqdISW-GxhyY3Op0sBU97C"


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


def handle_offer(urls: list[str], broadcaster: Broadcaster, parser: Union[Parser, None] = None,
                 parser_factory: Union[ParserFactory, None] = None):
    for url in urls:
        parser = parser_factory.get_parser_with_url(url) if parser_factory else parser
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

        import asyncio
        asyncio.run(broadcaster.broadcast(msg))


if __name__ == '__main__':
    user_args = parse_args()
    parser_factory = ParserFactory()
    broadcaster = Broadcaster()
    broadcaster.attach_all([StandardOutputNotifier(), DiscordNotifier(DISCORD_WEBHOOK)])

    if parser_urls := user_args.urls_file:
        for parser_name in parser_urls:
            handle_offer(parser_urls[parser_name], broadcaster=broadcaster,
                         parser=parser_factory.get_parser_with_id(parser_name))
    else:
        if not user_args.parser:
            handle_offer(user_args.urls, broadcaster=broadcaster, parser_factory=parser_factory)
        else:
            handle_offer(user_args.urls, broadcaster=broadcaster,
                         parser=parser_factory.get_parser_with_id(user_args.parser))

    history.commit()
