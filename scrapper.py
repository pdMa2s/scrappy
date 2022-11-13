from discord import SyncWebhook

import history
from parsers import AmazonParser, DigitecParser, OttosParser

webhook = SyncWebhook.from_url(
    "https://discord.com/api/webhooks/1041461946429472818/"
    "uOWyh5rcYqZwcxbcY3cIUxsZwIyJMWfU63-lN8AomJKRIXK_Yg6VTdW17uzxOr1XD64-"
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

if __name__ == '__main__':
    parsers = [DigitecParser(websites['Digitec']), AmazonParser(websites["Amazon"]), OttosParser(websites['Ottos'])]
    for p in parsers:
        for offer in p.get_offers():
            if not offer.price:
                print(f"Failed request to {p.__str__()[:-6]} try to fetch the link: {offer.link}")
                webhook.send(f"Failed request to {p.__str__()[:-6]} try to fetch the link: {offer.link}")
            else:
                last_price = history.get_price(offer.link)
                if last_price and last_price < offer.price:
                    print(f"{p.__str__()[:-6]}:  ----- Price reduction!!! ----\n\t\t{offer.product}"
                          f"\n\t\t- Link: {offer.link}\n\t\t- Price: {offer.price}")
                    webhook.send(f"{p.__str__()[:-6]}:  ----- Price reduction!!! ----\n\t\t{offer.product}"
                                 f"\n\t\t- Link: {offer.link}\n\t\t- Price: {offer.price}")
                elif not last_price:
                    print(f"{p.__str__()[:-6]}:\n\t\t{offer.product}\n\t\t- Link: {offer.link}"
                          f"\n\t\t- Price: {offer.price}")
                    webhook.send(f"{p.__str__()[:-6]}:\n\t\t{offer.product}\n\t\t- Link: {offer.link}"
                                f"\n\t\t- Price: {offer.price}")
                history.store_price(offer.link, offer.price)
    history.commit()
