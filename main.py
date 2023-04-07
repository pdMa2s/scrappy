import argparse
import os

from discord import Embed, Intents
from discord.ext import commands
from argparse import Namespace

from pasers import ParserFactory
from scheduler import JobScheduler
from storage import ProductDatabase


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(description='Scrappy Bot')
    parser.add_argument('-t', '--token', help='Discord Bot Token', default=os.environ.get('SCRAPPY_TOKEN'))
    args = parser.parse_args()
    assert args.token, 'Bot token is required'
    return args


intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

product_db = ProductDatabase("scrappy.db")
scheduler = JobScheduler()
parser_factory = ParserFactory()


def scrape_url(url: str):
    parser = parser_factory.get_parser_with_url(url)
    assert parser and parser.can_process_url(url)
    product = parser.get_product_info(url)
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


@bot.command(name="remove", help="Removes a product from the list of tracked products")
async def remove_product(ctx: commands.Context, url: str):
    product = product_db.get_product(url)
    if product:
        product_db.remove_product(product)
        await ctx.send(f"Removed product: {url}")
    else:
        await ctx.send(f"Product not found: {url}")


@bot.command(name="list", help="Lists the products that are being tracked")
async def list_product_prices(ctx: commands.Context):
    products = product_db.get_all_products()
    if not products:
        await ctx.send("No products found.")
    else:
        embed = Embed(title='Product Prices')
        for product in products:
            embed.add_field(name=f"{product.name} -> {product.current_price if product.has_price() else 'NO PRICE'}",
                            value=product.url, inline=False)
        await ctx.send(embed=embed)


@bot.command(help="Schedule a time for the bot to retrieve the prices and list them")
async def schedule(ctx: commands.Context, hour: int):
    async def scrape_and_list():
        scrape_all_urls()
        products = product_db.get_all_products()
        c = bot.get_channel(1041809388534513785)
        await c.send("test")

    scheduler.add_job(scrape_and_list, hour=hour)
    await ctx.send(f"I'll show the prices at {hour:02d} o'clock")


@bot.command(help="Removes one of the scheduled prices retrievals and listing")
async def remove_schedule(ctx: commands.Context, job_id: str):
    if scheduler.remove_job(job_id):
        await ctx.send(f"Removed job {job_id}")
    else:
        await ctx.send(f"Job {job_id} not found")


@bot.command(help="Lists all the schedules for the price retrievals")
async def list_schedules(message: commands.Context):
    if jobs := scheduler.list_jobs():
        response = f"Here are the current schedules:\n"
        response += "\n".join([f" -> {j}" for j in jobs])
        await message.channel.send(response)
    else:
        await message.channel.send("You have nothing scheduled currently :(")

if __name__ == '__main__':
    user_args = parse_args()
    try:
        bot.run(user_args.token)
    finally:
        scheduler.shutdown()
