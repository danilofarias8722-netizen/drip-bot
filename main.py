import discord
import os
from discord import app_commands

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    # Registra o comando só no teu servidor - instantâneo
    await tree.sync(guild=discord.Object(id=1498859204696346755))
    print(f'Bot {bot.user} online!')
    print('/loja registrado com sucesso!')

@tree.command(name="loja", description="Abre a loja do servidor")
async def loja(interaction: discord.Interaction):
    await interaction.response.send_message("Loja funcionando! 🛒")

# Pega o token escondido do Railway
bot.run(os.getenv("TOKEN"))
