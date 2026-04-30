import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot online!')
    try:
        synced = await bot.tree.sync()
        print(f'Comandos registrados: {len(synced)}')
    except Exception as e:
        print(f'Erro ao sincronizar: {e}')

@bot.tree.command(name="loja", description="Abre a loja")
async def loja(interaction: discord.Interaction):
    await interaction.response.send_message("Loja aberta! 🎉")

bot.run(os.getenv("DISCORD_TOKEN"))
