import discord
from discord import Intents
from discord.ext import commands

from product import Product
from scheduler import JobScheduler
from storage import ProductDatabase


class Scrappy(discord.Client):
    def __init__(self, product_db: ProductDatabase, job_scheduler: JobScheduler):

        super().__init__(command_prefix='!', intents=intents)
        self.product_db = product_db
        self.job_scheduler = job_scheduler

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        # start the scheduler when the bot is ready
        self.job_scheduler.start()

    async def on_message(self, message, *args):
        print(message.content)
        if message.author == self.user:
            return
        if message.content.startswith('!help'):
            await self.list_commands(message)
        elif message.content.startswith('!add'):
            await self.add_product(message, *args)
        elif message.content.startswith('!remove'):
            await self.remove_product(message, *args)
        elif message.content.startswith('!list'):
            await self.list_products(message)
        elif message.content.startswith('!add_notification'):
            await self.add_job(message, *args)
        elif message.content.startswith('!remove_notification'):
            await self.remove_job(message, *args)
        elif message.content.startswith('!list_notifications'):
            await self.list_jobs(message)
        elif message.content.startswith('!'):
            await message.channel.send("I don't understand that command :(")
            await self.list_commands(message)

    async def add_product(self, message, url: str):
        try:
            product = Product(url=url)
            self.product_db.add_product(product)
            await message.channel.send(f"Added product: {url}")
        except:
            await message.channel.send(f"Could not add product: {url}")

    async def remove_product(self, message, url: str):
        product = self.product_db.get_product(url)
        if product:
            self.product_db.remove_product(product)
            await message.channel.send(f"Removed product: {url}")
        else:
            await message.channel.send(f"Product not found: {url}")

    async def list_products(self, message):
        products = self.product_db.get_all_products()
        if not products:
            await message.channel.send("No products found.")
        else:
            response = "Product list:\n"
            for product in products:
                response += f"{product.url} ({product.name}): {product.current_price if product.current_price else ''}\n"
            await message.channel.send(response)

    async def add_job(self, message, hour: int, minute: int):
        self.job_scheduler.add_job(self.list_products, hour=hour, minute=minute)
        await message.channel.send(f"I'll show the prices at {hour:02d}:{minute:02d}")

    async def remove_job(self, message, job_id: str):
        if self.job_scheduler.remove_job(job_id):
            await message.channel.send(f"Removed job {job_id}")
        else:
            await message.channel.send(f"Job {job_id} not found")

    async def list_jobs(self, message: commands.Context):
        if jobs := self.job_scheduler.list_jobs():
            response = f"Here are the current jobs\n"
            response += "\n".join(jobs)
            await message.channel.send(response)
        else:
            await message.channel.send("You have no jobs currently :(")

    async def list_commands(self, message):
        help_str = "List of available commands:\n"
        help_str += "!help - Show this message\n"
        help_str += "!ping - Pong!\n"
        help_str += "!echo <message> - Echo back the message\n"
        await message.channel.send(f"\n{help_str}")
