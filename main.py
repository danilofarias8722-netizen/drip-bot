import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot online: {bot.user}')

@bot.command()
async def loja(ctx):
    embed = discord.Embed(
        title="🛍️ LOJA DRIP",
        description="Clique no botão abaixo para acessar a loja:",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
