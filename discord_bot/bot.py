import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def fetch(ctx, url):

    await ctx.channel.send(f'You said: {url}')

bot.run('MTA4MjcxOTAxNzI3MTMxMjM4NQ.GqCCnA.1Q7at9Ds4TabiETtdKKLKdcbCSVHuyLTWbv6q8')
