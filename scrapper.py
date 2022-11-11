from discord import SyncWebhook

from parsers import AmazonParser, DigitecParser

webhook = SyncWebhook.from_url(
    "https://discord.com/api/"
    "webhooks/1036384939878387723/pYZwx78HUlMxUv_6Br2kEsp69hQrxzzDqYz4UnWLn5qHs4hOptoF6IHLOswSqIKZ1h4T"
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
    ]
}

if __name__ == '__main__':
    parsers = [DigitecParser(websites['Digitec']), AmazonParser(websites["Amazon"])]
    for p in parsers:
        for offer in p.get_offers():
            if offer.price is None:
                print(f"Failed request to {p.__str__()[:-6]} try to fetch the link: {offer.link}")
                webhook.send(f"Failed request to {p.__str__()[:-6]} try to fetch the link: {offer.link}")
            else:
                print(f"{p.__str__()[:-6]}:\n\t\t{offer.product}\n\t\t- Link: {offer.link}"
                      f"\n\t\t- Price: {offer.price}")
                webhook.send(f"{p.__str__()[:-6]}:\n\t\t{offer.product}\n\t\t- Link: {offer.link}"
                             f"\n\t\t- Price: {offer.price}")

