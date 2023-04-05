from discord.ext import commands
from discord import Intents
from product import Product
from storage import ProductDatabase


class Scrappy(commands.Bot):
    def __init__(self, product_db: ProductDatabase):
        intents = Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self.product_db = product_db

    @commands.command(name='add')
    async def add_product(self, ctx: commands.Context, url: str):
        try:
            product = Product(url=url)
            self.product_db.add_product(product)
            await ctx.send(f"Added product: {url}")
        except:
            await ctx.send(f"Could not add product: {url}")

    @commands.command(name='remove')
    async def remove_product(self, ctx: commands.Context, url: str):
        product = self.product_db.get_product(url)
        if product:
            self.product_db.remove_product(product)
            await ctx.send(f"Removed product: {url}")
        else:
            await ctx.send(f"Product not found: {url}")

    @commands.command(name='list')
    async def list_products(self, ctx: commands.Context):
        products = self.product_db.get_all_products()
        if not products:
            await ctx.send("No products found.")
        else:
            message = "Product list:\n"
            for product in products:
                message += f"{product.url} ({product.name})\n"
            await ctx.send(message)


if __name__ == '__main__':
    product_db = ProductDatabase('product.db')
    bot = Scrappy(product_db=product_db)

    bot.run('MTA4MjcxOTAxNzI3MTMxMjM4NQ.GqCCnA.1Q7at9Ds4TabiETtdKKLKdcbCSVHuyLTWbv6q8')
