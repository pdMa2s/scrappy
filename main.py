import argparse
import os
from argparse import Namespace

from discord import Embed, Intents
from discord.ext import commands, tasks

from pasers import ParserFactory
from storage import ProductDatabase


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(description='Scrappy Bot')
    parser.add_argument('-t', '--token', help='Discord Bot Token', default=os.environ.get('SCRAPPY_TOKEN'))
    parser.add_argument('-c', '--channel_id', help='The channel to where the bot will show the product prices.'
                                                   ' If not provided it will default to the first guild\'s channel.',
                        default=None, type=int)
    args = parser.parse_args()
    assert args.token, 'Bot token is required'
    return args


channel_id = None
intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

product_db = ProductDatabase("scrappy.db")
parser_factory = ParserFactory()


def scrape_url(url: str):
    parser = parser_factory.get_parser_with_url(url)
    assert parser and parser.can_process_url(url)
    product = parser.get_product_info(url)
    if product.has_price():
        product_db.update_price(product)
    return product


def scrape_all_urls():
    for url in product_db.get_all_urls():
        scrape_url(url)


@bot.command(name="add", help="Adds a product to be tracked")
async def add_product(ctx: commands.Context, url: str):
    try:
        product = scrape_url(url)
        product_db.add_product(product)
        await ctx.send(f"Added product: {url}")
    except Exception as e:
        await ctx.send(f"Could not add product: {url}\n{e}")
        raise e


@bot.command(name="remove", help="Removes a product from the list of tracked products")
async def remove_product(ctx: commands.Context, url: str):
    product = product_db.get_product(url)
    if product:
        product_db.remove_product(product)
        await ctx.send(f"Removed product: {url}")
    else:
        await ctx.send(f"Product not found: {url}")


def get_product_prices() -> Embed:
    products = product_db.get_all_products()
    embed = Embed(title='Product Prices')
    if not products:
        embed.add_field(name="No products found", value=":(")
        return embed
    else:
        for product in products:
            embed.add_field(name=f"{product.name} -> {product.current_price if product.has_price() else 'NO PRICE'}",
                            value=product.url, inline=False)
        return embed


@bot.command(name="list", help="Lists the products that are being tracked")
async def list_product_prices_command(ctx: commands.Context):
    await ctx.send(embed=get_product_prices())


@tasks.loop(hours=12)
async def list_product_prices_task():
    scrape_all_urls()
    await bot.get_channel(channel_id).send(embed=get_product_prices())


@bot.command(help="Set a time interval in hours for the bot to retrieve the prices and list them")
async def interval(ctx: commands.Context, hours: int):
    list_product_prices_task.change_interval(hours=hours)
    await ctx.send(f"I'll show the prices every {hours:02d} hours")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    global channel_id
    if not channel_id:
        channel_id = bot.guilds[0].text_channels[0].id
    list_product_prices_task.start()


if __name__ == '__main__':
    user_args = parse_args()
    channel_id = user_args.channel_id
    bot.run(user_args.token)